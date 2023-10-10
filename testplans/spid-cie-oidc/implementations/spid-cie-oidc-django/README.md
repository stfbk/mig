# spid-cie-oidc-django implementation

## changes wrt original repo

With respect to the original docker compose found in the repo, we added i-mig-t, which contains Burp Suite, a proxy able to intercept HTTP messages between the containers. From now on the group of containers of spid-cie-oidc-django and i-mig-t will be called **infrastructure**.
To intercept all the HTTP messages, the compose file responsible has been modified and, in particular, a network configuration capable of redirecting all the HTTP messages intended for the other containers towards the Burp proxy has been added.

## Quickstart

Before starting configure a proper DNS resolution for the following domain names. In GNU/Linux we can configure it by inserting in `/etc/hosts` the following string:

```bash
127.0.0.1   localhost  trust-anchor.org relying-party.org cie-provider.org
```

To execute the infrastructure follow the steps depending on your OS:

### linux

<details>
The infrastructure can be executed on linux using the two `.sh` files provided:

- `build_and_run.sh` This file is useful when changes to the files are made or it is the first time that the infrastructure is run. It clones the [original repository](https://github.com/italia/spid-cie-oidc-django), applies some changes to the configuration, builds the proxy container (file [burpsuite_container/Dockerfile](burpsuite_container/Dockerfile)) and runs all together.

- `run.sh` It runs the infrastructure directly, without cloning the repo or applying changes.

If in doubt, this command will always work:

```bash
bash build_and_run.sh
```

</details>

### windows

<details>
Execute the infrastructure with the Windows Subsystem for Linux, using the same command defined for Linux.

</details>

### MacOS (ARM)

<details>
This infrastracture cannot be executed on ARM processors. Hopefully, an ad-hoc version will be provided soon.
</details>

## Using MIG-T

When the infrastructure is running, [MIG-T](https://github.com/stfbk/mig-t) can be used. It requires two inputs:

- **Session:**
- **Machine-Readable (MR) Tests:**

refer to [this readme](/tools/i-mig-t/readme.md#using-mig-t) for details.

### Sessions

Test normally use the session `s_CIE` which provides a basic login and logout flow. Nonetheless, other sessions can be found:

- **s1-logout:** base session without the logout;
- **s1-credentials:** base session without the insertion of the credentials.

In MIG the text of the file corresponding to the defined session must be used.

### MR tests

In the linked folder you can find an implementation of the tests defined in the [xlsx file](/testplans/spid-cie-oidc/Testplan%20-%20SPID%20CIE%20OIDC%20v2.0.xlsx) (where also a description and other additional information can be found for each test). In each implementation file there will be a test suite containing one or more tests implementations, with also a name and a description. In the aforementioned folder there are different files named as a pattern that can group different tests. A description of each pattern can be found in [patterns](patterns.md).  
Some files does not belong to a pattern, though, which means that were written by hand. This files are inside the folder [handmade](/testplan/machine-readable-testplan/handmade) and the filename starts with the entity interested by the test (OP/RP/SA/TA/AA).

#### Supported machine-readable Tests

In the release v2.0, we designed and executed 483 tests out of 800.

The following tests are excluded:

- Tests involving Attribute Authority (AA) or Subject Aggregators (SA).
- Tests not reported in `\testplans\spid-cie-oidc\implementations\spid-cie-oidc-django\input\mig-t\tests`

### Message definition

mig-t on burp works by intercepting HTTP messages of interest for the test and performing actions and checks on them. In order to intercept the right HTTP message, a correct definition is needed and this can be found in the [message definition file](config/mig-t/msg_def.json). In this file a specific configuration for this infrastructure is given, so the names (URLs) "relying-party.org", "trust-anchor.org" and "cie-provider.org" are used. If you want to add some HTTP messages to be intercepted you need to add them on the message definition file

## Known Bugs

When running the infrastructure, it can happen that burp exits with a 0 error code. It will be enough to re-run the infrastructure to fix it. A real fix should come soon.

### OIDC Federation Profile Tests

When performing tests related to the OIDC Federation profile, it is necessary to restart the environment for each active test individually. However, if the tests are passive, they can all be executed together. To identify whether a test pertains to OIDC Federation, you should check the 'profile' column in the testplan [link](/testplans/spid-cie-oidc/). To determine whether a test is active or passive, you should examine the 'type' tag in the test's JSON file [link](testplans/spid-cie-oidc/implementations/spid-cie-oidc-django/input/mig-t/tests).
To restart only the environment, you can execute the following command:

```sudo bash restart_django.sh```

## Cleaning

After using the infrastructure several times, it is likely that the space occupied by the docker cache is quite huge. It could be useful to run directly `docker system prune` to prune all objects together or, alternatively, to run `docker builder prune` (which will free the docker cache that occupies most of the space) and perform single objects [pruning](https://docs.docker.com/config/pruning/) if necessary.
