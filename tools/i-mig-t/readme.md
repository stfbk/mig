# i-mig-t
integrated mig-t is a docker image containing
- mig-t
- Burpsuite Community Edition
- A browser

it offers a simple way to integrate mig-t into a Docker environment, allowing you to intercept all messages from the Docker environment and execute tests in mig-t.

## Architectures
The i-mig-t tool does not yet fully support ARM devices. However, a specially-crafted Docker image is being developed. This image can be used to run i-mig-t on ARM devices, but there are still some problems with the x-forwarding of the GUI to the host OS, especially for Apple users.

## Getting started
To use i-mig-t, you can use either the Docker image hosted on the GitHub registry or build it yourself using the build.sh script. Regardless of the image you choose, you need to create a docker-compose.yml file that includes the i-mig-t image and your environment images. Make sure to properly configure the network interfaces so that the i-mig-t container can intercept all traffic between all containers. You also need to configure all containers to use the Burp proxy (port 8080) inside the i-mig-t container. For an example on how this could be done, check the implementation inside the spid-cie-oidc tesplan.

> Remember to activate xhost access on host machine (xhost +local:)

If you want to run the container without using the docker-compose file, use this command
```
docker run --rm -it --name burpsuite -e DISPLAY -v /tmp/.X11-unix/:/tmp/.X11-unix/ -v /etc/localtime:/etc/localtime:ro --volume="$HOME/.Xauthority:/root/.Xauthority:rw" --volume="/run/dbus/system_bus_socket:/run/dbus/system_bus_socket" proxy
```