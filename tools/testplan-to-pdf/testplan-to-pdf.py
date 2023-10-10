import pandas as pd
from fpdf import FPDF
import os
from os.path import dirname, join

ROOT_DIR_PATH = dirname(os.path.abspath(__file__))

INPUT_DIR_PATH = join(ROOT_DIR_PATH, "input")
OUTPUT_DIR_PATH = join(ROOT_DIR_PATH, "output")

FILENAME_INPUT = "testplan.csv"
FILENAME_OUTPUT = "testplan.pdf"
INPUT_FILE_PATH = join(INPUT_DIR_PATH, FILENAME_INPUT)
OUTPUT_FILE_PATH = join(OUTPUT_DIR_PATH, FILENAME_OUTPUT)

def _info(ans: str):
    """
    Simple print on file of info

    :param ans: the selected element to print info
    :type ans: str

    :return: Nothing
    """

    description = ""

    if ans == "AA":
        ans = "Attribute Authority"
        description = "The Attribute Authority (AA) handler of the qualified attribues (Leaf Entity)."
    elif ans == "OP":
        ans = "OpenID Provider"
        description = "The OpenID Provider (OP) is defined as the OAuth 2.0 Authorization Server that is capable of Authenticating the End-User and providing Claims to a Relying Party about the Authentication event and the End-User."
    elif ans == "RP":
        ans = "Relying Party"
        description = "The Relying Party (RP) is defined as the OAuth 2.0 Client application requiring End-User Authentication and Claims from an OpenID Provider."
    elif ans == "SA":
        ans = "Intermediary Anchor"
        description = "The Intermediary Anchor (SA), Intermediate Entity or Intermediary. An intermediate Entity that can handle all the Federation aspects of one or more RPs."
    elif ans == "TA":
        ans = "Trust Anchor"
        description = "The Trust Anchor (TA), OIDC Federation Trust Anchor."
    elif ans == "ALL":
        description = "Tests available for all the entities."

    return ans, description

def _create_if_not_exist(path: str):
    """Creates a folder or file given a path.

    Args:
      path: The path to the folder or file to create.
    """

    if os.path.exists(path):
        # The path already exists, so do nothing.
        return

    if os.path.isdir(path):
        # The path is a directory, so create it.
        os.makedirs(path)
    else:
        # The path is a file, so create it.
        d = dirname(path)

        os.makedirs(d, exist_ok=True)

        open(path, "w").close()

def main():
        
    _create_if_not_exist(INPUT_FILE_PATH)

    # Load the CSV file
    df = pd.read_csv(INPUT_FILE_PATH)

    df = df[['UID', 'Test Name', 'Description', 'Entity under test', 'Message Under test', 'Input to test', 
            'Input to Entity Under Test', 'Output', 'Profile', 'Requirement', 'Requirement Source']]

    # Remove rows with NaN values in the columns you're interested in
    df = df.dropna(subset=['Entity under test', 'Test Name', 'Description', 'Profile'])

    # Create a new PDF
    pdf = FPDF(format='A4')

    # Set the line height for each cell
    line_height = 5

    # Iterate over the DataFrame, grouping by the column that corresponds to "Title1" and "Title2" in your PDF
    for eut, group in df.groupby('Entity under test'):
        # Add a new page for each group
        pdf.add_page()

        title, description = _info(eut)

        # Add the title and the hardcoded short description
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, title)
        pdf.ln()
        pdf.set_font('Arial', '', 12)
        pdf.multi_cell(0, line_height, description)
        pdf.ln()

        # Iterate over the rows in the group, adding the subtitle and the values from columns 3 and 4
        for _, row in group.iterrows():
            pdf.set_font('Arial', 'B', 14)
            pdf.multi_cell(0, line_height, row['Test Name'].encode('latin-1', 'replace').decode('latin-1'))
            pdf.ln()

            # Iterate over the columns and dynamically create the rows
            for col in df.columns:
                if col != 'Test Name' and col != 'Entity under test': 
                    pdf.set_font('Arial', '', 12)
                    pdf.multi_cell(0, line_height, col+': ' + str(row[col]).encode('latin-1', 'replace').decode('latin-1'))
                    pdf.ln()

    _create_if_not_exist(OUTPUT_FILE_PATH)

    # Save the PDF
    pdf.output(OUTPUT_FILE_PATH, 'F')

if __name__ == "__main__":

    main()
