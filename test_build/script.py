#!/usr/bin/python3

import argparse
import csv
from typing import Iterator


# --- columns ---

COL_UID = 'UID'
COL_MSG = 'Input for generated MR: message to handle'
COL_ORACLE = 'Input for generated MR: Oracle'


# --- defaults ---

GENERATE_INPUT_FILE = 'testplan.csv'
GENERATE_OUTPUT_FILE = 'suite.template.csv'

# --- generate ---

def generate(input_file, output_file):
    # read data from file
    with open(input_file if input_file is not None else GENERATE_INPUT_FILE) as f:
        reader = csv.DictReader(f)
        rows = [r for r in reader]

    # expand rows (one line of the input file can represent more than one test template)
    expanded_rows = []
    for r in rows:
        expanded_rows.extend(expand_row(r))
    
    print(data[:5])

def expand_row(row: dict) -> Iterator[dict]:
    # uid tokens
    uid_tokens = row[COL_UID].split('-')
    msg_tokens = row[COL_MSG].split('-')
    oracle_tokens = row[COL_ORACLE].split('-')
    
    # expand by uid
    if '_' in uid_tokens[0]:
        yield row.copy()

    # expand by message
    if '_' in msg_tokens[0]:
        pass
    


    # return row



# --- compile ---

def compile(partial, input_file, output_file, compilation_params):
    pass


# --- execute ---

def execute(partial, input_file, output_file):
    pass


# --- common ---

def main():
    parser = argparse.ArgumentParser(
        description="Generates tests for OpenID Connect SPIC/CIE",
    )

    # filters
    parser.add_argument('--filter', '-f', action='append', nargs=2, type=str, metavar=('COLUMN', 'VALUE'),
                        help="perform actions only on tests that match the filers")

    # actions
    parser.add_argument('--generate',   '-g', action='store_true', default=False,
                        help="generate test templates from testplan")
    parser.add_argument('--compile',    '-c', action='store_true', default=False,
                        help="compile test templates into executable tests")
    parser.add_argument('--execute',    '-e', action='store_true', default=False,
                        help="perform tests in MIG-T")

    # common input/output
    parser.add_argument('--input',  '-i', action='store', type=str, metavar='FILE',
                        help='the input file for the first action to be performed (it overrides the value in --input-[generate | compile | execute])')
    parser.add_argument('--output', '-o', action='store', type=str, metavar='FILE',
                        help='the output file for the last action to be performed (it overrides the value in --output-[generate | compile | execute])')
    
    # specific input/output
    parser.add_argument('--input-generate',     action='store', type=str, metavar="FILE",
                        help="the testplan as CSV")
    parser.add_argument('--output-generate',    action='store', type=str, metavar='FILE',
                        help="the test suite with test templates")
    
    parser.add_argument('--input-compile',      action='store', type=str, metavar='FILE',
                        help="the test suite with test templates")
    parser.add_argument('--output-compile',     action='store', type=str, metavar='FILE',
                        help="the test suite with executable tests")
    parser.add_argument('--compilation-params', action='store', type=str, metavar='FILE',
                    help="parameters used in test compilations")

    
    parser.add_argument('--input-execute',      action='store', type=str, metavar='FILE',
                        help="the test suite with executable tests")
    parser.add_argument('--output-execute',     action='store', type=str, metavar='FILE',
                        help="the result after executing of the test suite")
    
    # parse arguments
    args = parser.parse_args()

    # run all if the user has not selected a section
    if not (args.generate or args.compile or args.execute):
        args.generate = True
        args.compile = True
        args.execute = True

    # override inputs
    if args.generate and args.input is not None:
        args.input_generate = args.input
        args.input = None

    if args.compile and args.input is not None:
        args.input_compile = args.input
        args.input = None
    
    if args.execute and args.input is not None:
        args.input_execute = args.input
        args.input = None

    # override outputs
    if args.execute and args.output is not None:
        args.output_execute = args.output
        args.output = None

    if args.compile and args.output is not None:
        args.output_compile = args.output
        args.output = None

    if args.generate and args.output is not None:
        args.output_generate = args.output
        args.output = None

    # DEBUG
    print(args)

    # execute sections
    partial = None

    # generate
    if args.generate:
        partial = generate(args.input_generate, args.output_generate)

    # compile
    if args.compile:
        partial = compile(partial, args.input_compile, args.output_compile, args.compilation_params)
    
    if args.execute:
        execute(partial, args.input_compile, args.output_compile)


# keep this block at the end of the file
if __name__ == '__main__': 
    main()
