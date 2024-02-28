# testplan-to-mr

## Overview

This tool reads test data from a CSV file, filters and processes it, generates JSON files, and stores them in an output directory. It also handles exceptions and logs errors during execution.

## Summary

* [How to execute testplan-to-mr](#how-to-execute-testplan-to-mr)
* [Constraints](#constraints)

## How to execute testplan-to-mr

### Using the image hosted on github registry

```bash
docker pull ghcr.io/stfbk/mig-testplan-to-mr:master
```

### Building the image by yourself

<details>

Build the Docker image using the following command:

```bash
docker build -t testplan-to-mr .
```

</details>

### Execute testplan-to-mr

To execute the docker image you can use this command:

```bash
docker run \
 --rm \
 -v path_to_testplan_implementation_folder_:/testplan-to-mr/input \
 -v path_to_output_folder:/testplan-to-mr/machine-readable-testplan/single \
 testplan-to-mr 
```

Otherwise, inside each implementation you can find a generate_mr.sh file that will convert the given testplan to mr.

Furthermore, this script offers two optional command-line options, that can be added in the execution of either docker or bash script, to customize the test generation process:

1. `--justFill <input_path>`. This flag enables the script to only populate the testplans, from the provided input_path folder, with the information extracted from the configuration file.
2. `--django`. This flag includes additional information related to the Django session in the generated tests.

## Detailed description

### Dockerfile description

This Dockerfile does the following:

1. It starts with the official Python 3.10.11 base image.
2. Sets the working directory to `/testplan-to-mr` within the container.
3. Copies the `requirements.txt` file from the host into the container's working directory.
4. Installs Python dependencies from `requirements.txt` using `pip`.
5. Copies the `testplan-to-mr.py` script from the host into the container's working directory.
6. Specifies the command to run when a container is started, which is to execute the `testplan-to-mr.py` script using Python.

### Python Structure

The provided Python script is creating and managing JSON files based on data stored in CSV files. Here is an architectural overview of the script:

1. **Import Statements**: The script begins by importing various Python libraries and modules, including `copy`, `logging`, `sys`, `os`, `pandas` (for data manipulation), and `regex` (for regular expressions).

2. **Global Constants**: There is a global constant defined as `OUT_DIR`, which specifies the output directory where the generated JSON files will be stored.

3. **Exception Handling**: There is an exception handling function (`handle_exception`) defined to handle uncaught exceptions and log error messages.

4. **Utility Functions**:
   * `_check_key_exists`: A function that checks if a key exists in a nested dictionary and can rename it.
   * `_check_value_exists`: A function that checks if a value exists in a nested dictionary and can replace it.

5. **`createTestsfromCsv` Function**: This function is the main driver of the script and takes a list of entities, patterns, and a DataFrame of tests. It iterates through the entities and patterns, filters the data, creates JSON objects for tests, and writes them to files.

6. **`createJson` Function**: This function creates JSON structures for individual tests based on the filtered data for a specific entity and pattern. It processes test data from the DataFrame and replaces values in predefined JSON templates.

7. **`createPassive` Function**: A function designed for creating passive tests based on a specific type ("Passive"). It operates similarly to `createTestsfromCsv` but focuses on passive tests.

8. **`main` Function**: The main function of the script. It reads the test data from a CSV file, prompts the user to specify entities and patterns for test creation, and calls the `createTestsfromCsv` and `createPassive` functions.

9. **Script Execution**: The script includes a section that sets the working directory and configures logging for errors. It also defines an exception hook using the `handle_exception` function. Finally, it calls the `main` function to initiate the JSON files creation process.

## Constraints

The script takes a CSV file as input and applies filters to the columns named "Entity under test" and "Pattern name," automatically including the available values and adding an "ALL" option.

To generate the JSON files, the tool need the following information:

1. **A CSV file** with the following columns:

   * *Test Name*: Contains the name of the test.
   * *Description*: Contains the description of the test.
   * *Input for generated MR: Oracle* and/or *Input for generated MR: message to handle*: Contains the sorted variables to populate the JSON file. The first is used for intercept operations, and the second is used for validation.
   * *UID*: Contains a unique identifier for each row.
   * *Pattern name*: Contains the name of the pattern.
   * *Entity under test*: Contains the entity to evaluate.
   * *Type*: Describes if the test is correct or involves incorrect input.

2. **Templates** named as *Type*-*Pattern name*.json, json file defined as "key_name":"varx", where x is a progressive number from 0 to 9 then, from 10, is "_x". *varx* is a variable name that the script automatically assigns and whose value changes depending on the input.

### Notes

1. If "/" or "" are present in the pattern name, the row will be ignored by the process (e.g., when there is no template).
2. The variables taken by the script are split by " | ".
