import logging  # used for errors
import os
import re  # used in avoidMd_errors()
import sys

import pandas as pd
from m2r import parse_from_file


# System function - shouldn't need update as the table changed.
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


def avoidMd_errors(var: dict) -> dict:
    """
    Escape special characters that will not be readed by the md

    :param var: the value to be modified
    :type var: str

    :return: the modified value
    """

    for k, v in var.items():
        # find where there is something that could be interpreted as an inline html or it will not appear in the document
        if isinstance(v, str):

            # modify the strange accent
            var[k] = v.replace(chr(8217), "'")

            if "<" in v and ">" in v:
                var[k] = v.replace("<", "\<")

            # find the urls "http *** /" and escape them <> add "+/$" for ending in case
            if "http" in v:
                temp = re.findall(r'(https?://[^\s]+$)', v)
                for e in temp:
                    var[k] = var[k].replace(e, "<" + e + ">")

            if "- " in v:
                temp = re.findall('(- [A-Z][\s\S]*?(?:\n|\.))', v)
                if temp:
                    var[k] = var[k].replace(":\n", ":<ul>\n")
                for e in temp:
                    var[k] = var[k].replace(e, "<li>" + e[2:].strip() + "</li>")
                if temp:
                    var[k] = var[k].replace(">\n    <", "><") + "</ul>"

            if re.findall(r"\d\.\s", v):
                temp = re.findall('(\d\.\s[A-Z][\s\S]*?(?:\n|\.))', v)
                if temp:
                    var[k] = var[k].replace(": \n", ":<ol>")
                for e in temp:
                    var[k] = var[k].replace(e, "<li>" + e[2:].strip() + "</li>")
                if temp:
                    var[k] = var[k].replace(">\n    <", "><") + "</ol>"

    return var


if __name__ == "__main__":
    """
    Creation of a Test Plan based on an Excel file
    """
    logging.basicConfig(filename='./Output/cvsToPdf.log',
                        level=logging.DEBUG,
                        format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')

    sys.excepthook = handle_exception

    try:
        wd = sys._MEIPASS
    except AttributeError:
        wd = os.getcwd()

    md_filepath = os.path.join(wd, ".", "Output")
    rst_filepath = os.path.join(wd, "..", "docsItalia", "docs")

    # returns a DATAFRAME from csv test plan
    df = pd.read_csv(os.path.join(wd, "Input", "testplan.csv"))

    # remove useless spaces 
    df = df.replace(os.linesep, regex=True)

    # create new DataFrame and only keep columns of interest
    df = df[['UID', 'Entity under test', 'Test Name', 'Description', 'Profile', 'Requirement', 'Requirement Source',
             'Input', 'Output', 'Affected Message']]

    # dropping the rows having NaN values
    df = df.dropna(subset=['Requirement'])

    # reset the indices
    df = df.reset_index(drop=True)

    entity_under_test = ['RP', 'TA', 'SA', 'OP']
    logging.debug("Generating test plan for " + ",".join(entity_under_test))

    # For each Entity Under Test, create a md file and convert it to rst file. 
    for entity in entity_under_test:

        # Filter the original dataframe (from csv) by the "Entity under test"
        df_entity = df[df['Entity under test'] == entity]

        md_fname = os.path.join(md_filepath, entity.lower() + ".md")
        rst_fname = os.path.join(rst_filepath, entity.lower() + ".rst")
        file_output = open(md_fname, "w")
        file_output.write(os.linesep)
        file_output.write(f"# Test plan for {entity} \n")

        logging.debug("Opening the file " + md_fname)
        # For each row (test case) in the filtered dataframe, extract the test in a Series format and then convert it in md table
        for ii in range(df_entity.shape[0]):
            df1 = df_entity.iloc[ii]

            df1.name = ""
            sec_title = df1["UID"]
            file_output.write(f"## {sec_title} \n\n")
            df1 = df1.drop(["UID", "Entity under test"])

            # for removing and modifying values transform the series into a dictionary with the value as row values and key as the header
            var = df1.to_dict()
            var = avoidMd_errors(var)

            # convert dict to series for md table conversion
            df2 = pd.Series(var)
            df2.name = ""

            # Convert series to md table and write to file
            file_output.write(df2.to_markdown())
            file_output.write(os.linesep * 4)

        file_output.close()
        logging.debug("Closing the file " + md_fname)

        # Finally, parse the md file and convert it to rst file (in the docsItalia folder)
        output_rst = parse_from_file(md_fname)
        file_output_rst = open(rst_fname, "w")
        logging.debug("Opening the file " + rst_fname)
        file_output_rst.write(output_rst)
        file_output_rst.close()
        logging.debug("Closing the file " + rst_fname)
        logging.debug("Total number of test for " + entity.lower() + " is:" + str(df_entity.shape[0]))