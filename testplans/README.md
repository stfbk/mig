# Overview

This folder contains all the testplans supported by MIG, categorized by the type of protocol or standard.

## Folder Structure

```bash
testplans
├── testplan_name
│   ├── config
│   │   └── testplan-to-mr
│   │       └── templates
│   ├── implementations
│   │   ├── implementation_name
│   │   │   ├── input
│   │   │   │   ├── mig-t
│   │   │   │   │   ├── sessions
│   │   │   │   │   └── tests
│   │   │   │   └── testplan-to-mr
│   │   │   └── config
│   │   │   │   ├── mig-t
│   │   │   │   │   └── msg_def.json
│   │   │   │   └── testplan-to-mr
│   │   │   │       └── config_testplan.json
│   │   │   └── generate_mr.sh
```

In this folder, each testplan is accompanied by a dedicated subfolder. Within each testplan folder resides a "testplan.csv" file containing the actual testplan. Furthermore, an "implementations" folder is present, encompassing all implementations currently supported by this testplan.

An implementation serves as software that executes the protocols addressed within the testplan. Each testplan can be executed across all available implementations. The reason for the divergence in testplan execution across implementations lies in the variability of messages, keys, and other factors among the different implementations. Consequently, machine-readable tests may require slight adjustments to function seamlessly with each implementation.

For each implementation, machine-readable tests are provided in the input/mig-t/tests/ folder. These tests are expressed as individual JSON files, each representing a single test case. These machine-readable tests correspond to a subset of the tests documented in the human-readable test plan.

It is essential to maintain the default folder structure within each "testplan_name" folder to ensure the correct operation of the scripts.
