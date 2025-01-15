# MIG

Micro-Id-Gym (MIG) is a flexible and extendable tool designed to assist system administrators and security testers in conducting
security testing on Identity Management (IdM) protocol implementations. MIG provides both a [toolsuite for penetration testing](tools/) and [testplans for IdM protocol implementations](testplans/).

A testplan for a protocol/standard, also known as a human readable testplan, comprises a set of specifications written in a format that is easily understandable by humans. It outlines the tests required to validate the compliance of a specific protocol/standard. MIG currently offers a human readable testplan that covers the OIDC protocol.

As for the tools, MIG offers a seamless testing environment known as i-mig-t, a script designed to enhance the readability of the human readable testplan by converting it into PDF format, a script to translate the majority of the human readable tests into a machine-readable format compatible with the security testing tool, MIG-T, and integration of the spid-cie-oidc-django implementation from Developers Italia.

## Summary

* [What is in this Repo](#what-is-in-this-repo)
* [Quickstart](#quickstart)
* [Definitions](#definitions)
* [Using MIG](#using-mig)
* [Contributing](#contributing)
* [Credits](#credits)
* [References](#references)
* [License](#license)

## What is in this Repo

```bash
mig
├── tools
│   ├── mig-t (submodule)
│   ├── i-mig-t
│   ├── testplan-to-mr
│   └── testplan-to-pdf
└── testplans
    └── spid-cie-oidc
        └── implementations
            └── spid-cie-oidc-django
```

### tools

The tool folder provides a testing environment, useful scripts and all the available tools of mig. Following is a brief description of each tool available:

* [__mig-t__](https://github.com/stfbk/mig-t): a semi-automated security testing tool provided as a [BurpSuite Community Edition](https://portswigger.net/burp/communitydownload) (Burp) extension based on a declarative language for security testing. It is provided as a git submodule. To access additional information, kindly consult [this link](https://github.com/stfbk/mig-t/blob/main/README.md).
* __i-mig-t__: stands for integrated mig-t and includes a Docker image containing Burp, [Mozilla Firefox](https://www.mozilla.org/en-US/firefox/), and mig-t. For more details, please refer to [this link](tools/i-mig-t/readme.md).
* __testplan-to-mr__: a script to convert the testplan from a human readable format into machine-readable format for mig-t. To access further information, please visit [this link](tools/testplan-to-mr/readme.md).
* __testplan-to-pdf__: a script for converting the human readable testplan into a PDF format to improve readability. For additional details, please visit [this link](tools/testplan-to-pdf/readme.md).

### tesplans

This folder aims to contain the specifications of testplans for IdM protocols/standards. For each IdM protocol/standard a human readable testplan is provided in CSV format. Currently, the following testplans are available in MIG:

* spid-cie-oidc: this testplan is focusing on SPID/CIE OIDC and based on [SPID/CIE OpenID Connect Regole tecniche](https://docs.italia.it/italia/spid/spid-cie-oidc-docs/it/versione-corrente/index.html)

### implementations

For each IdM protocol/standard, a human readable test plan is made available. Each IdM protocol/standard may encompass one or more implementations. The available implementations are located in this folder. Below, you'll find a brief description of the currently available implementations:

* spid-cie-oidc-django: [spid-cie-oidc-django implementation](https://github.com/italia/spid-cie-oidc-django) provided by Developers Italia.

## Quickstart

MIG currently supports the spid-cie-oidc testplan along with the implementation of [spid-cie-oidc-django](https://github.com/italia/spid-cie-oidc-django). To execute MIG with spid-cie-oidc testplan against the spid-cie-oidc-django implementation, please refer to the [folder](testplans/spid-cie-oidc/implementations/spid-cie-oidc-django/) and consult the provided [readme](testplans/spid-cie-oidc/implementations/spid-cie-oidc-django/README.md).

## Definitions

* __session__: is a list of user actions which can be seen as a UI integration test that testers use to create for web applications and which inherits the Selenium engine and its primitives.

* __human readable test__: test cases or test specifications that are defined in a way that can be easily understood by humans, particularly testers, developers, project managers, and other stakeholders who may not have specialized technical knowledge. The human readable version of the tests prioritize clarity, simplicity, and comprehensibility, making them accessible to a broad audience without the need for deep technical expertise.

* __machine readable test__: test cases or test specifications that are formatted and structured in a way that can be interpreted, and executed by automated testing tools, scripts, or software programs. These tests are designed in JSON format and ready to be parsed and executed by [MIG-T](tools/mig-t).

## Using MIG

### To get started with MIG-T

Please refer to the following guides:

* For executing a testplan, please consult [this readme](tools/i-mig-t/readme.md#using-mig-t).
* In a generic scenario, refer to [this readme](https://github.com/stfbk/mig-t/blob/main/README.md).

### How to execute testplan-to-mr

Please follow the guidelines reported [here](/tools/testplan-to-mr/readme.md).

### How to execute testplan-to-pdf

Please follow the instructions reported [here](/tools/testplan-to-pdf/readme.md).

## Contributing

Our project welcomes contributions from various types of users, each with unique ways to contribute. We appreciate contributions from users of all types, and together, we can make our project even better! Here's a list of potential user types and the guidelines on the actions they can take to participate in our project:

### User who wants to run machine-readable tests on SPID/CIE Django implementation

<details>
<summary>Instructions</summary>

* To get started, follow the instructions to run `i-mig-t`.
* In [testplans/spid-cie-oidc/implementations/spid-cie-oidc-django/input/mig-t/tests/](testplans/spid-cie-oidc/implementations/spid-cie-oidc-django/input/mig-t/tests), you can find a list of all available and supported machine-readable tests.
* In [testplans/spid-cie-oidc/implementations/spid-cie-oidc-django/input/mig-t/sessions/](/testplans/spid-cie-oidc/implementations/spid-cie-oidc-django/input/mig-t/sessions), you can find related sessions.

</details>

### User who wants to test their own implementation of SPID/CIE OIDC

<details>
<summary>Instructions</summary>

A guide on how to add your RP to the testing environment can be found [here](testplans/spid-cie-oidc/README.md#adding-support-for-your-relying-party)

</details>

## Using mig-t in Headless Mode

1. Start MIG-T in headless mode, for example with the command `build_and_run.sh` inside the folder `mig/testplans/spid-cie-oidc/implementations/spid-cie-oidc-django/`
2. Run the script `run_tests.sh`, passing a test in JSON format or an acronym representing an entity from spid-cie-oidc-django (OP, RP, TA) as a parameter to execute the test suite containing all the tests for that entity. You can also add the `-p` option to execute only the passive tests for that entity
3. The output of the testing will be saved in the `output.json` file within the context in which the `run_tests.sh` command is executed. For the case of `spid-cie-oidc-django` the file will be in the folder `mig/testplans/spid-cie-oidc/implementations/spid-cie-oidc-django/`

For more information about mig-t, please follow the guidelines reported [here](https://github.com/stfbk/mig-t/blob/main/README.md)

## Details on the image for Headless Mode

<details>
This Docker architecture is designed to create a containerized environment for running Burp Suite Community Edition and MIG-t, along with the necessary dependencies to facilitate web application testing using Selenium with Firefox. Here's a description of the architecture:

**Base Image:**
The Docker image is based on Ubuntu 22.04, providing a stable and well-established Linux distribution as the foundation for the containerized environment.

**Package Installation:**
The Dockerfile begins by updating the package repository and installing various essential packages such as `wget`, `bzip2`, and Java Development Kit (JDK) components to support the execution of Burp Suite and other required software. Additionally, it installs `curl` and `jq` to run the `run_test.sh` script file.

**Burp Suite Installation:**
The Dockerfile automates the installation of Burp Suite Community Edition by downloading the specified version from PortSwigger's CDN. It makes the necessary setup to place Burp Suite in the `/opt/BurpSuiteCommunity/` directory within the container.

**Selenium and Firefox Setup:**
The Docker image includes Selenium WebDriver support by downloading and configuring the GeckoDriver for Firefox. It also downloads and installs a specific version of the Firefox browser in the `/opt/` directory and creates a symbolic link to it in `/usr/bin/`.

**Cache Avoidance:**
A random data download from "<https://www.random.org/cgi-bin/randbyte?nbytes=10&format=h>" is included to prevent Docker from caching files that could change frequently.

**File Copying:**
The Docker image copies several configuration and application files into the container, including MIG-T a Java application JAR file (`mig-t-beta-jar-with-dependencies.jar`) and Burp Suite configuration files (`project-options.json` and `user-options.json`). These files are placed in the appropriate directories within the container.

**Container Start Command:**
The Docker image specifies the command to run when the container is started. It launches Burp Suite Community Edition in headless mode with specific configuration files (`user-options.json` and `project-options.json`) using the command `java -Djava.awt.headless=true -jar \
/opt/BurpSuiteCommunity/burpsuite_community.jar`. The -Djava.awt.headless=true option enables headless mode, which allows Burp Suite to run without a graphical user interface. To disable headless mode, remove the -Djava.awt.headless=true option. The command also includes a confirmation prompt (echo 'y') to automatically accept the terms of service.

Overall, this Docker architecture creates a containerized environment for web application security testing that is fully capable of running in headless mode. By combining Burp Suite with Firefox and Selenium WebDriver, it provides a streamlined and reproducible solution for security professionals and developers who need to automate tests and operate without a graphical user interface.

</details>

### User who wants to add a human readable test plan for another IdM protocol

<details>
<summary>Instructions</summary>

To contribute a test plan for a different IdM protocol, please adhere to the [repository's structure](testplans/README.md#folder-structure) within the `testplan` folder.

* Create a `readme.md` file containing information about the test plan you wish to add.
* The added test plan file should have a `.csv` extension and include all the columns specified in the [testplan.csv](testplans/spid-cie-oidc/testplan.csv) file.

</details>

### User who wants to modify a human readable test plan for SPID/CIE OIDC

<details>
<summary>Instructions</summary>

To propose changes or enhancements to the existing SPID/CIE OIDC test plan located in [/testplans/spid-cie-oidc/](/testplans/spid-cie-oidc/), kindly initiate discussions by creating issues directly within the repository or by submitting a pull request.

</details>

### User who wants to modify MIG and mig-t

<details>
<summary>Instructions</summary>

To facilitate improvements or modifications to MIG, consider the following options:

* Initiate discussions by opening issues to propose new features or report any identified bugs.
* Actively participate in improving the source code by submitting a pull request.

To contribute to `mig-t`, please consult its dedicated [repository](https://github.com/stfbk/mig-t).

</details>

### Others

<details>
<summary>Instructions</summary>

* For contributions falling into a category not mentioned above, feel free to reach out to us at <a.bisegna@fbk.eu> through our communication channels. We welcome all forms of contribution and collaboration.

</details>

## Credits

1. [Burp Suite Community Edition](https://portswigger.net/burp/communitydownload)
2. [Mozilla Firefox](https://www.mozilla.org/en-US/firefox/new/)
3. [spid-cie-oidc-django](https://github.com/italia/spid-cie-oidc-django)

## References

1. [Micro-Id-Gym - Identity Management Workouts with Container-Based Microservices](https://st.fbk.eu/tools/Micro-Id-Gym.html)
1. Andrea Bisegna (PhD Thesis, University of Genova, 2023) Automated Security Testing for Identity Management of Large-scale Digital Infrastructures
1. Matteo Bitussi (Bachelor's Thesis, University of Trento, 2022) [Declarative Specification of Pentesting Strategies for Browser-based Security Protocols: the Case Studies of SAML and OAuth/OIDC](https://github.com/mattebit/thesis/blob/main/Bitussi_Matteo_Informatica_21.pdf)
1. Alessandro Biasi (Bachelor's Thesis, University of Trento, 2022) Syntax And Semantics Of A Declarative Language For Security Testing Of Browser Based Security Protocols

## License

Everything in this repository is licensed under the [Apache 2.0 license](LICENSE)

```text
Copyright 2023, Fondazione Bruno Kessler

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```

Designed and developed within [Security & Trust](https://st.fbk.eu/) Research Unit at [Fondazione Bruno Kessler](https://www.fbk.eu/en/) (Italy) in cooperation with [Istituto Poligrafico e Zecca dello Stato](https://www.ipzs.it/) (Italy) and Futuro & Conoscenza.
