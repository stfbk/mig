from copy import deepcopy
import sys
import os
from os.path import join
import pandas as pd
import regex as re
import json
import logging #used for errors
import argparse #used for args

"""
    Idea: there is a test suite created for each entity and for each type. 
    The program takes the test suite and populates the parameter "tests" with the tests created. Previous tests are deleted.
"""

OUT_DIR_SINGLE = "tests/single/"
DIR_TEMPLATES = "/testplan-to-mr/input/templates/"

# Specify the input folder and output folder paths for the config
INPUT_TEST = 'tests'
OUTPUT_TEST = 'configured_tests'

class TestGenerator:
    "Class that handles lists, e.g., replace values, check existence and substitute, duplicate"
    def __init__(self, input_dir, output_dir):
        self.input_dir = input_dir
        self.output_dir = output_dir
    
    @staticmethod
    def _replace_value(row:pd, old_value:str, toIterate:list):
        new_rows = []
        if isinstance(toIterate, str):
            toIterate = toIterate.split("_")
        for e in toIterate:
            new_row = row.copy()  # Copy the original row
            for col in row.index:
                if pd.notna(new_row[col]) and old_value in str(new_row[col]):
                    new_row[col] = new_row[col].replace(old_value, e)
                if pd.notna(new_row[col]) and "Entity Configuration response" in str(new_row[col]) and not re.search(r'Entity Configuration response [A-Z]{2}\b', str(new_row[col])):
                    new_row[col] = new_row[col].replace("Entity Configuration response", "Entity Configuration response "+e)
            new_rows.append(new_row)
        return new_rows

    def _check_key_exists(self, d: dict, key:str, new_value):
        """
        Check if a key exists in a nested dictionary recursively.
        """

        if key in d:
            d[new_value]=d.pop(key)
            return
        else:
            for k, v in d.items():
                if isinstance(v, dict):
                    self._check_key_exists(v, key, new_value)
                elif isinstance(v, list):
                    for item in v:
                        if isinstance(item, dict):
                            self._check_key_exists(item, key, new_value)

    def _check_value_exists(self, d: dict, old_value:str, new_value):
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
                self._check_value_exists(v, old_value, new_value)
            elif isinstance(v, list):
                for index, item in enumerate(v):
                    if isinstance(item, dict):
                        self._check_value_exists(item, old_value, new_value)
                    if isinstance(item, str) and old_value in item:
                        v[index] = item.replace(old_value, new_value)

    def process_row(self, row: pd.DataFrame) -> list:
        # Duplicate when Entity1_Entity2
        """
        This function duplicates rows based on certain conditions in the 'UID' and 'Entity under test' columns.
        It handles the following scenarios:
        1. When 'UID' contains "_": duplicates the row for each uid_parts[0].split('_').
        2. When 'UID' contains "ALL" in part[0]: duplicates the row for each entity in entitites
        3. When 'UID' contains "ALL" in part[0]: duplicates the row for each entity in entitites - the entity in parts[0]
        """
        uid_parts = row['UID'].split('-')
        message = ""
        oracle = ""
        
        if isinstance(row.get('Input for generated MR: message to handle'), str):
            message = row.get('Input for generated MR: message to handle').split('|')[0]
        if isinstance(row.get('Input for generated MR: Oracle'), str):
            oracle = row.get('Input for generated MR: Oracle').split('|')[0]
        
        new_row = []
        if "_" in uid_parts[0]:
            new_row.extend(self._replace_value(row, uid_parts[0], uid_parts[0]))
        if "_" in message:
            message_ent = list(set(re.findall(r'\b\w*_\w*\b', message)))
            if len(message_ent) < 2:
                message_ent = message_ent[0]
                new_row.extend(self._replace_value(row, message_ent, message_ent))
            else:
                raise ValueError("Multiple entities were found in Input for generated MR: message to handle")
        if "_" in oracle:
            oracle_ent = list(set(re.findall(r'\b\w*_\w*\b', oracle)))
            if len(oracle_ent) < 2:
                oracle_ent = oracle_ent[0]
                new_row.extend(self._replace_value(row, oracle_ent, oracle_ent))
            else:
                raise ValueError("Multiple entities were found in Input for generated MR: Oracle")
            
        else:
            new_row.append(row)

        # Substitute ALL with the single entity
        new_rows = []
        for rows in new_row:
            entities = ["TA", "SA", "AA", "OP", "RP"]
            if "ALL" in rows['UID']:
                if "ALL" in uid_parts[1] and "ALL" not in uid_parts[0]:
                    entities.remove(rows['UID'].split('-')[0])
                if "ALL" in uid_parts[0] and "_" in message: #ALL the entities are removed
                    entities = [item for item in entities if item not in message_ent.split('_')]
                if "ALL" in uid_parts[0] and "_" in oracle: #ALL the entities are removed
                    entities = [item for item in entities if item not in oracle_ent.split('_')]
                new_rows.extend(self._replace_value(rows, "ALL", entities))
            else:
                new_rows.append(rows)
        
        return new_rows
    
    def create_json(self, table: pd.DataFrame, entity: str) -> list:
        """
            This function creates the Jsons of the tests that will be added to the file of the corresponding test testType and entity. 
            All the characteristics of the test suite must already be in the file, this function only creates tests (in the "tests" 
            claim) and insert in the file.
            The input is a DataFrame containing the portion of the table filtered for an entity.
            The output is a list of the JSON structures composing the tests
        """

        tests = []

        for index, row in table.iterrows():
            """
            Look in the filtered table taking the json written as 'type_name-pattern_name.json' per row
            When found an existing file use it, else skip to the next row.
            """

            testType = [t.lower().replace(" ", "_") for t in set(table["Type"])][0]
            
            filename = testType+"-"+row["Pattern name"]

            try:
                openfile = open(os.path.join(DIR_TEMPLATES, f'{filename}.json'), 'r')
            except(FileNotFoundError):
                log_pattern.debug(f'[ERROR] TemplateNotFound: {filename}.json')
                continue
            
            message_split = "" if pd.isna(row["Input for generated MR: Oracle"]) else row["Input for generated MR: Oracle"].split(" | ")
            messageTH_split = "" if pd.isna(row["Input for generated MR: message to handle"]) else row["Input for generated MR: message to handle"].split(" | ")

            if message_split:

                if messageTH_split:
                    message_split = messageTH_split + message_split

                message_split = [row["Test Name"]] + [row["Description"]] + message_split

                #handling errors
                global flag

                message_split = [msg.replace("X_key_ALL", "X_key_"+entity) if "X_key_ALL" in msg else msg for msg in message_split]
                message_split = [msg.replace("X_url_ALL", "X_key_"+entity) if "X_url_ALL" in msg else msg for msg in message_split]
                
                used_item = deepcopy(message_split)

                template = json.load(openfile)
                
                for index, item in enumerate(message_split):
                    flag = False
                    var = "var"+str(index) if index < 10 else "var_"+str(index)
                    if "body" in message_split and item == "body":
                        self._check_key_exists(template, "key_"+var, "check regex")
                        self._check_key_exists(template, "edit_"+var, "edit regex")
                    elif "url" in message_split and item == "url":
                        self._check_key_exists(template, "key_"+var, "check")
                        self._check_key_exists(template, "edit_"+var, "edit")
                    else:
                        self._check_key_exists(template, "key_"+var, "check param")
                        self._check_key_exists(template, "edit_"+var, "edit")
                    
                    # Check if EC is specified and fill the template                     
                    if var == "var2" and (item == "Entity Configuration response"):
                        generator._check_value_exists(template, var, item + " " + entity)
                    else:
                        self._check_value_exists(template, var, item)
                    
                    if flag:
                        used_item.remove(item)

                    if s_django:
                        self._check_value_exists(template, "session0", row["Session in spid-oidc-cie-django"])

                #check for missing inserted values in the list
                if len(used_item) != 0:
                    log_value.warning(f'Values not inserted {used_item} for Pattern: {row["Pattern name"]} and UID: {row["UID"]}')

                #check for missing inserted values in the template
                temp = re.findall(r"var\d|var_\d{2}",str(template))
                if temp:
                    log_value.warning(f'Values missing in table {temp} for Pattern: {row["Pattern name"]} and UID: {row["UID"]}')

                #print a test suite for each row if not ALL
                t = []
                t.append(template)
                singleSuite = {"test suite":{"name":"Single test" , "description":"One test only" ,"filter messages": True}, "tests":t}
                json_objects = json.dumps(singleSuite, indent = 2)
                processor._create_if_not_exist(join(OUT_DIR_SINGLE, entity))
                with open(os.path.join(wd, OUT_DIR_SINGLE+'/'+entity, f'{row["UID"]}.json'), 'w') as outfile:
                        outfile.write(json_objects)

                tests.append(template)

            #if exists but its empty
            else:
                log_pattern.warning(f'Empty test on Pattern: {row["Pattern name"]} and UID: {row["UID"]}')
        
        return tests

class FileProcessor:
    "Class to work with folders, e.g., checking existence, creating and traverse them"
    def __init__(self, input_dir, output_dir):
        self.input_dir = input_dir
        self.output_dir = output_dir
    
    @staticmethod
    def _create_if_not_exist(path: str):
        """Creates a folder or file given a path"""
        if not os.path.exists(path):
            os.makedirs(path)

    def traverse_folder(self, substitutions):
        for root, dirs, files in os.walk(INPUT_TEST):
            for file in files:
                if file.endswith('.json'):
                    file_path = os.path.join(root, file)

                    # Load the JSON document
                    try:
                        with open(file_path, 'r') as f:
                            data = json.load(f)
                    except ValueError:
                        print(f"Error in file: {file_path}")
                        continue

                    # Substitute
                    for key, value in substitutions.items():
                        generator._check_value_exists(data, key, value)

                    # Create the output file path that copies the input
                    output_file_path = os.path.join(OUTPUT_TEST, (file_path.split(INPUT_TEST,1)[1]).lstrip(os.path.sep))
                    self._create_if_not_exist(os.path.dirname(output_file_path))

                    with open(output_file_path, 'w') as output_file:
                        json.dump(data, output_file, indent=2)

class ConfigLoader:
    "Class to handle and parse configuration file, in this case it is used only at the end to personalize the JSONs"
    def config_for_implementation(self):
        # Load JSON config file
        with open('config_file/config_testplan.json', 'r') as f:
            substitutions = json.load(f)
        
        processor._create_if_not_exist(OUTPUT_TEST)

        # Call the function to traverse the folder and modify the JSON files
        processor.traverse_folder(substitutions)

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
    session_test = []
    entity_test = []

    # Filter for the entity (rows where entity under test = entity)
    for entity in entities:
        # Filter for the type of the test
        for pattern in patterns:
            # Returns the rows where entity under test is the entity and the type of the column is the wanted type
            filtered = df_tests[((df_tests["Entity under test"] == entity)) 
                                & (df_tests["Pattern name"] == pattern)]

            tests = generator.create_json(filtered, entity)

            if tests:
                session_test.extend(tests)
                entity_test.extend(tests)     
        
        #Test by entity
        entitySuite = {"test suite":{"name":entity , "description":"All the test available for this entity" ,"filter messages": True}, "tests":entity_test}
        json_objects = json.dumps(entitySuite, indent = 2)
        if entity_test and entity != "ALL":
            with open(os.path.join(wd, OUT_DIR_SINGLE+'/'+entity, f'All_{entity}.json'), 'w') as outfile:
                    outfile.write(json_objects)
        entity_test = []
    
    testSuite = {"test suite":{"name":"Session" , "description":f"All the entities" ,"filter messages": True}, "tests":session_test}
    json_objects = json.dumps(testSuite, indent = 2)
    with open(os.path.join(wd, OUT_DIR_SINGLE, 'ALL_Sessions.json'), 'w') as outfile:
        outfile.write(json_objects)

    # Extract Passive            
    passive_objects = [obj for obj in session_test if (isinstance(obj, dict) and obj.get("test") and obj.get("test").get("type") == "passive")]
    passiveSuite = {"test suite":{"name":"Passive" , "description":"All the passive" ,"filter messages": True}, "tests":passive_objects}
    passive_json = json.dumps(passiveSuite, indent=2)
    with open(os.path.join(wd, OUT_DIR_SINGLE, 'Passive.json'), 'w') as outfile:
        outfile.write(passive_json)

def generate_mr():
    #Returns a dataframe
    df_tests = pd.read_csv(os.path.join(wd, "input", "testplan.csv"))

    # Process each row and expand the DataFrame
    expanded_rows = []
    for _, row in df_tests.iterrows():
        expanded_rows.extend(generator.process_row(row))

    # Create a new DataFrame from the processed rows
    df_tests = pd.DataFrame(expanded_rows)
    
    entitiesToTest = [x for x in list(set(df_tests["Entity under test"])) if str(x) != "nan"]
    patternsToTest = [item for item in list(set(df_tests["Pattern name"])) if isinstance(item, str) and "/" not in item]

    # Create filtered dataframe
    createTestsfromCsv(entitiesToTest, patternsToTest, df_tests)

if __name__ == "__main__":
    """
    Take the position of the working directory and set out logging for errors
    """
    # Usage
    generator = TestGenerator(INPUT_TEST, OUTPUT_TEST)
    processor = FileProcessor(INPUT_TEST, OUTPUT_TEST)
    config_loader = ConfigLoader()
    
    try:
        wd = sys._MEIPASS
    except AttributeError:
        wd = os.getcwd()

    logging.basicConfig(level = logging.DEBUG,
                format = '%(asctime)s:%(levelname)s:%(name)s:%(message)s')
    
    log_pattern = logging.getLogger('testplan.pattern')
    log_value = logging.getLogger('testplan.missingValue')

    parser = argparse.ArgumentParser()

    # Add the --justFill flag with 1 args <input>
    parser.add_argument('--justFill', nargs=1, help='Specify input_path of test, the script will traverse folder for json')
    # Add the '--django' argument
    parser.add_argument('--django', action='store_true', help='Add django sessions')
    s_django = False

    args = parser.parse_args()
    if args.justFill:
        INPUT_TEST = args.justFill[0]
        config_loader.config_for_implementation()
        print("Configured tests")
    else:
        processor._create_if_not_exist(OUT_DIR_SINGLE)
        if args.django:
            s_django = True
        generate_mr()
        print("Generated tests")
        config_loader.config_for_implementation()
        print("Configured tests")

    print("END.")
