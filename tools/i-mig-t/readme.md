# Overview

i-mig-t stands for integrated mig-t, it is a Docker image containing:

- [mig-t](https://github.com/stfbk/mig-t)
- [Burp Suite Community Edition](https://portswigger.net/burp/communitydownload)
- [Mozilla Firefox](https://www.mozilla.org/en-US/firefox/)

i-mig-t provides a straightforward method for integrating mig-t into a Docker environment, enabling you to intercept HTTP messages within the Docker environment and conduct tests using mig-t

## Summary

- [Getting started](#getting-started)
- [Using mig-t](#using-mig-t)
- [Details on the image](#details-on-the-image)
- [Problems fixing](#problems-fixing)
- [Known Issues](#known-issues)

## Getting started

### Use the docker image hosted on github registry

To use i-mig-t, you can choose either the [Docker image](https://github.com/stfbk/mig/pkgs/container/mig-i-mig-t) hosted on the GitHub registry

```bash
docker pull ghcr.io/stfbk/mig-i-mig-t:master
```

### Build the docker image yourself

<details>

Before building the image, you need to get the mig-t jar, you can browse the [release page of mig-t](https://github.com/stfbk/mig-t/releases) and get version you need, or you can just execute [mig-t-jar-compile.sh](mig-t-jar-compile.sh) that will init the mig-t submodule and compile the jar for you.

> compiling the jar of mig-t requires maven

Either way you choose, at the end you should have the mig-t-beta-jar-with-dependencies.jar file in this folder.

To build the image you can use the following script

```bash
build.sh
```

or just

```bash
docker build -t i-mig-t .
```

</details>

### Adding i-mig-t container to your environment

We suggest creating a `docker-compose.yml` file that includes the i-mig-t image and your environment images. Ensure proper configuration of the network interfaces to allow i-mig-t container to intercept all traffic between all containers. Additionally, configure all containers to use the Burp proxy (port 8080) inside the i-mig-t container.

> Remember to activate xhost access on host machine (xhost +local:)

### Run the container standalone

If you want to run the container standalone, use this command:

```bash
docker run --rm -it --name burpsuite -e DISPLAY -v /tmp/.X11-unix/:/tmp/.X11-unix/ -v /etc/localtime:/etc/localtime:ro --volume="$HOME/.Xauthority:/root/.Xauthority:rw" --volume="/run/dbus/system_bus_socket:/run/dbus/system_bus_socket" proxy
```

## Using mig-t

1. Go to the "MIG-T" tab in Burp
2. Click on "Use Firefox," then select "Driver" and choose "geckodriver" in the pop-up window
3. Copy the content of the session you need, usually found inside the implementation you are using in the folder `input/mig-t/sessions/`
4. Copy the tests you need inside the "input JSON" textbox. The tests are the machine-readable tests, that are usually find inside the implementation you are using in the folder `input/mig-t/tests`
5. Click the "Read JSON" button
6. Click the "Execute Test Suite" button
7. View the results in the "Test Suite Result" tab

For more information about mig-t, please follow the guidelines reported [here](https://github.com/stfbk/mig-t/blob/main/README.md)

## Details on the image

<details>
This Docker architecture is designed to create a containerized environment for running Burp Suite Community Edition and MIG-t, along with the necessary dependencies to facilitate web application testing using Selenium with Firefox. Here's a description of the architecture:

**Base Image:**
The Docker image is based on Ubuntu 22.04, providing a stable and well-established Linux distribution as the foundation for the containerized environment.

**Package Installation:**
The Dockerfile begins by updating the package repository and installing various essential packages such as `wget`, `bzip2`, and Java Development Kit (JDK) components to support the execution of Burp Suite and other required software.

**Environment Configuration:**
The Docker image sets the `DISPLAY` environment variable, enabling graphical user interface (GUI) interactions within the container.

**Burp Suite Installation:**
The Dockerfile automates the installation of Burp Suite Community Edition by downloading the specified version from PortSwigger's CDN. It makes the necessary setup to place Burp Suite in the `/opt/BurpSuiteCommunity/` directory within the container.

**Selenium and Firefox Setup:**
The Docker image includes Selenium WebDriver support by downloading and configuring the GeckoDriver for Firefox. It also downloads and installs a specific version of the Firefox browser in the `/opt/` directory and creates a symbolic link to it in `/usr/bin/`.

**Cache Avoidance:**
A random data download from "<https://www.random.org/cgi-bin/randbyte?nbytes=10&format=h>" is included to prevent Docker from caching files that could change frequently.

**File Copying:**
The Docker image copies several configuration and application files into the container, including MIG-T a Java application JAR file (`mig-t-beta-jar-with-dependencies.jar`) and Burp Suite configuration files (`project-options.json` and `user-options.json`). These files are placed in the appropriate directories within the container.

**Container Start Command:**
The Docker image specifies the command to run when the container is started. It launches Burp Suite Community Edition with specific configuration files (`user-options.json` and `project-options.json`) using the command `./opt/BurpSuiteCommunity/BurpSuiteCommunity`.

Overall, this Docker architecture streamlines the setup of a containerized environment for web application security testing, combining Burp Suite with Firefox and Selenium WebDriver, making it a convenient and reproducible solution for security professionals and developers.

</details>

## Problems fixing

### Docker Installation

If you encounter issues with docker on linux while running i-mig-t, please be sure you have installed Docker using the apt repository method reported [here](https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository) and not trough the snap store.

## Known Issues

The i-mig-t tool currently lacks full support for ARM devices. Nevertheless, there is a specifically tailored Docker image accessible in the "arm" branch of the i-mig-t GitHub repository. This image enables the execution of i-mig-t on ARM devices, albeit there are ongoing issues related to GUI x-forwarding to the host OS, particularly impacting Apple users.
