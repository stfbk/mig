from copy import deepcopy
import sys
import os
from os.path import dirname, join
import pandas as pd
import regex as re
import json
import logging #used for errors

"""
    Idea: there is a test suite created for each entity and for each type. 
    The program takes the test suite and populates the parameter "tests" with the tests created. Previous tests are deleted.
"""

OUT_DIR_SINGLE = "machine-readable-testplan/single/"

#System function - shouldn't need update as the table changed.
def handle_exception(exc_type, exc_value, exc_traceback):
    """
    Handle the exception and print the traceback

    :param exc_type: the type of the exception
    :param exc_value: the value of the exception
    :param exc_traceback: the traceback of the exception

    :return: critical on the logging and stop the execution
    """

    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    logging.critical("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

    print("Some error occoured. Reporting to the administrator...\nPlease, restart the application.")

def _create_if_not_exist(path: str):
    """Creates a folder or file given a path.

    Args:
      path: The path to the folder or file to create.
    """

    if not os.path.exists(path):
        os.makedirs(path)

def _check_key_exists(d: dict, key:str, new_value):
    """
    Check if a key exists in a nested dictionary recursively.
    """

    if key in d:
        d[new_value]=d.pop(key)
        return
    else:
        for k, v in d.items():
            if isinstance(v, dict):
                _check_key_exists(v, key, new_value)
            elif isinstance(v, list):
                for item in v:
                    if isinstance(item, dict):
                        _check_key_exists(item, key, new_value)

def _check_value_exists(d: dict, old_value:str, new_value):
    """
    Check if a value exists in a nested dictionary recursively.
    """
    global flag
    for k, v in d.items():
        if isinstance(v, str) and old_value in v and new_value.startswith('["'):
            d[k] = new_value[2:len(new_value)-2].split('", "')
            flag = True
        elif isinstance(v, str) and old_value in v:
            d[k] = d[k].replace(old_value, new_value)
            flag = True
        if isinstance(v, dict):
            _check_value_exists(v, old_value, new_value)
        elif isinstance(v, list):
            for item in v:
                if isinstance(item, dict):
                    _check_value_exists(item, old_value, new_value)

def createTestsfromCsv(entities: list, patterns: str, df_tests: pd.DataFrame):
    """
        This function checks the csv of the testplan (total), iterates over the entities and the types of tests the user
        wants to create and calls the functions to create the jsons of the tests and to populate the test suite of the given
        entity and type of tests
        example of filtered data frame: (tests of type Correct generation for RP)
                            UID          Profile Entity under test  ... Note Has Reference Checked
                0   FED001  OIDC Federation                RP       ...  NaN         False     NaN
                17  FED018  OIDC Federation                RP       ...  NaN         False     NaN
                18  FED019  OIDC Federation                RP       ...  NaN         False     NaN
                25  COR001        OIDC Core                RP       ...  NaN         False       x
                26  COR002        OIDC Core                RP       ...  NaN         False       x

    """
    count = 0
    dict_sum = {}
    session1_test = []
    entity_test = []

    # Filter for the entity (rows where entity under test = entity)
    for entity in entities:
        # Filter for the type of the test
        for pattern in patterns:
            # Returns the rows where entity under test is the entity and the type of the column is the wanted type
            filtered = df_tests[((df_tests["Entity under test"] == entity) | (df_tests["Entity under test"] == "ALL")) 
                                & (df_tests["Pattern name"] == pattern)]

            tests, supported_pattern = createJson(filtered, pattern, entity)

            if tests:
                session1_test.extend(tests)
                entity_test.extend(tests)
        
        #Test by entity
        entitySuite = {"test suite":{"name":entity , "description":"All the test available for this entity" ,"filter messages": True}, "tests":entity_test}
        json_objects = json.dumps(entitySuite, indent = 2)
        if entity_test and entity != "ALL":
            with open(os.path.join(wd, OUT_DIR_SINGLE+'/'+entity, f'All_{entity}.json'), 'w') as outfile:
                    outfile.write(json_objects)
        entity_test = []
    
    testSuite = {"test suite":{"name":"Session_1" , "description":f"All the entities and the available patterns: {' ,'.join([*dict_sum.keys()])}" ,"filter messages": True}, "tests":session1_test}
    json_objects = json.dumps(testSuite, indent = 2)
    with open(os.path.join(wd, OUT_DIR_SINGLE, 'ALL_Session1.json'), 'w') as outfile:
        outfile.write(json_objects)

def createJson(table: pd.DataFrame, pattern: str, entity: str) -> list:
    """
        This function creates the Jsons of the tests that will be added to the file of the corresponding test testType and entity. 
        All the characteristics of the test suite must already be in the file, this function only creates tests (in the "tests" 
        claim) and insert in the file.
        The input is a DataFrame containing the portion of the table filtered for an entity.
        The output is a list of the JSON structures composing the tests
    """

    tests = []
    count_test = {}

    for index, row in table.iterrows():
        """
        Look in the filtered table taking the json written as 'type_name-pattern name.json' per row
        When found an existing file use it, else skip to the next row.
        """

        testType = [t.lower().replace(" ", "_") for t in set(table["Type"])][0]
        
        try:
            openfile = open(os.path.join(wd, "input", "implementations", "spid-cie-oidc-django", "config", "testplan-to-mr", "templates", f'{testType}-{row["Pattern name"]}.json'), 'r')
        except(FileNotFoundError):
            log_pattern.debug(f'TemplateNotFound: {testType}-{row["Pattern name"]}.json ')
            continue
        
        message_split = "" if pd.isna(row["Input for generated MR: Oracle"]) else row["Input for generated MR: Oracle"].split(" | ")
        messageTH_split = "" if pd.isna(row["Input for generated MR: message to handle"]) else row["Input for generated MR: message to handle"].split(" | ")

        if message_split:

            if messageTH_split:
                message_split = messageTH_split + message_split

            message_split = [row["Test Name"]] + [row["Description"]] + message_split

            #handling errors
            global flag
            used_item = deepcopy(message_split)

            template = json.load(openfile)
            
            for index, item in enumerate(message_split):
                flag = False
                var = "var"+str(index) if index < 10 else "var_"+str(index)
                if "body" in message_split and item == "body":
                    _check_key_exists(template, "key_"+var, "check")
                    _check_key_exists(template, "edit_"+var, "edit regex")
                else:
                    _check_key_exists(template, "key_"+var, "check param")
                    _check_key_exists(template, "edit_"+var, "edit")
                #Next if is for SPID                      
                if var == "var2" and (item == "Entity Configuration response" or item == "Entity Statement response"):
                    _check_value_exists(template, var, item + " " + entity)
                else:
                    _check_value_exists(template, var, item)
                if flag:
                    used_item.remove(item)

            #check for missing inserted values in the list
            if len(used_item) != 0:
                log_value.warning(f'Values not inserted {used_item} for Pattern: {row["Pattern name"]} and UID: {row["UID"]}')

            #check for missing inserted values in the template
            temp = re.findall(r"var\d|var_\d{2}",str(template))
            if temp:
                log_value.warning(f'Values missing in table {temp} for Pattern: {row["Pattern name"]} and UID: {row["UID"]}')

            #print a test suite for each row if not ALL
            if row['Entity under test'] != 'ALL':
                singleSuite = {"test suite":{"name":"Single test" , "description":"One test only" ,"filter messages": True}, "tests":template}
                json_objects = json.dumps(singleSuite, indent = 2)
                _create_if_not_exist(join(OUT_DIR_SINGLE, row["Entity under test"]))
                with open(os.path.join(wd, OUT_DIR_SINGLE+'/'+row['Entity under test'], f'{row["UID"]}.json'), 'w') as outfile:
                        outfile.write(json_objects)

            tests.append(template)

            count_test[row["Pattern name"]] = count_test.setdefault(row["Pattern name"],0 ) + 1
        #if exists but its empty
        else:
            log_pattern.warning(f'Empty test on Pattern: {row["Pattern name"]} and UID: {row["UID"]}')
    
    return tests, count_test

def main():
    #Returns a dataframe
    df_tests = pd.read_csv(os.path.join(wd, "input", "testplan.csv"))
    
    # Decide for which entity we want to create the tests
    entitiesToTest = "ALL" #input("Which entity do you want to test? (combinations separated by commas or ALL for all the entities) ").upper()
    if entitiesToTest == "ALL":
        entitiesToTest = [x for x in list(set(df_tests["Entity under test"])) if str(x) != "nan"]
        entitiesToTest.remove("ALL")
    else:
        entitiesToTest = entitiesToTest.split(',')
        for i in range(0, len(entitiesToTest)):
            entitiesToTest[i] = entitiesToTest[i].replace(" ", "")

    # Decide for which pattern we want to create the tests
    patternsToTest = "ALL" #input("Which type of test do you want to create? (combinations separated by commas or ALL for all the tests").upper()

    if patternsToTest == "ALL":
        patternsToTest = [item for item in list(set(df_tests["Pattern name"])) if isinstance(item, str) and "/" not in item]
    else:
        patternsToTest = patternsToTest.split(',')

    # Create filtered dataframe
    createTestsfromCsv(entitiesToTest, patternsToTest, df_tests)

if __name__ == "__main__":
    """
    Take the position of the working directory and set out logging for errors
    """

    try:
        wd = sys._MEIPASS
    except AttributeError:
        wd = os.getcwd()

    logging.basicConfig(level = logging.DEBUG,
                format = '%(asctime)s:%(levelname)s:%(name)s:%(message)s')
    
    log_pattern = logging.getLogger('testplan.pattern')
    log_value = logging.getLogger('testplan.missingValue')

    sys.excepthook = handle_exception

    _create_if_not_exist(OUT_DIR_SINGLE)

    main()

    print("END.")