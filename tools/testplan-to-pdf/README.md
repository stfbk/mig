# testplan-to-pdf

## Overview

The tool reads test data from a CSV file, filters and processes the data, generates MD file, and stores the PDF file in an output directory. It also handles exceptions and logs errors during execution.
The tool reads test data from a CSV file, filters and processes the data, generates MD file, and stores the PDF file in an output directory. It also handles exceptions and logs errors during execution.

## Summary

* [How to execute testplan-to-pdf](#how-to-execute-testplan-to-pdf)
* [Architectures](#architectures)
* [Content of the output](#content-of-the-output)

## How to execute testplan-to-pdf

### Using the image hosted on github registry

We have a ready-to-use image on the github registry, you can check it out here

```bash
docker pull ghcr.io/stfbk/mig-testplan-to-pdf:master
```

### Building the image yourself

<details>

you can just execute this script that will build the image and run it.

```bash
bash testplan2pdf.sh
```

or you can manually

```bash
sudo docker build -t testplan-to-pdf .
```

</details>

### Running the docker container

you can manually run this command

```bash
docker run \
    --rm \
    -v testplan_folder:/testplan-to-pdf/input \
    -v output_folder:/testplan-to-pdf/output \
    mig-testplan-to-pdf
```

and change the container name according to if you builded the image locally or you are using the pulled one.

## Architectures

Let's start by exploring the Dockerfile structure, which outlines the key components involved in containerizing applications, followed by an architectural overview of the provided Python script designed for generating the PDF file.

### Python Structure

The provided Python script is creating and managing an MD file based on data stored in CSV files. Here is an architectural overview of the script:

1. **Import Statements**: The script begins by importing various Python libraries and modules, including `copy`, `logging`, `sys`, `os`, `pandas` (for data manipulation), and `regex` (for regular expressions).

2. **Global Constants**: There is a global constant defined as `OUT_DIR`, which specifies the output directory where the generated JSON files will be stored.

3. **Exception Handling**: There is an exception handling function (`handle_exception`) defined to handle uncaught exceptions and log error messages.

4. **`main` Function**: The main function of the script. It writes information to the md file.

5. **Script Execution**: The script includes a section that sets the working directory and configures logging for errors. It also defines an exception hook using the `handle_exception` function. Finally, it calls the `main` function to initiate the JSON files creation process.

## Content of the output

The objective is to generate a testplan in PDF format from a human-readable testplan provided as input in CSV file format. This process involves converting the CSV file to Markdown (MD) format and subsequently to PDF. The testplan document, generated in PDF format, organizes all tests into categories based on entities. Each test provides the following information:

* **Title**: Name of the test
* **UID**: Unique Identifier
* **Description**: Description of the test
* **Message Under test**: The location or context where the test occurs
* **Input tester**: Input message for the test
* **Input EUT**: Input for the environment under test
* **Output**: Definition of the expected output of the test
* **Profile**: The profile to which the test belongs (e.g., OIDC Core or OIDC Federation)
* **Requirement**: The associated requirement
* **Requirement Source**: Link to the specification
