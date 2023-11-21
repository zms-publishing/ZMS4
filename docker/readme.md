# Running a ZMS Container with Docker

Important: *The here presented Docker environment is not recommended for production, just for testing and exploration.*

The ZMS source folder `./docker` contains two minimalistic Docker files: 
1. the [dockerfile](https://github.com/zms-publishing/ZMS4/blob/main/docker/dockerfile) for creating a Docker *image* and 
2. the [docker-compose](https://github.com/zms-publishing/ZMS4/blob/main/docker/docker-compose.yml) file for building a Docker *container*.

The image utilizes a minimal *alpine*-Linux with Python2 and some additional software packages (like mariadb and openldap). The ZMS installation happens with pip in a successively created virtual python environment (`/home/zope/venv`) and provides the ZMS code in the pip-"editable" mode. Both the ZMS source code (`/home/zope/venv/src/ZMS/.git`) and the Zope instance are placed in the virtual python environment folder (`/home/zope/venv/instance/zms4`)


## Running the ZMS Container with VSCode

The VSCode Docker Extension [ms-azuretools.vscode-docker](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-docker) is a perfect tool for handling containers. A right mouse click on the file ´docker-compose.yaml´ starts composing the container. Initially Zope will be started and Zope will run on port 8080.

## Attach VSCode to the ZMS Container
Another right click on the running container-ID allows to intrude the container with VSCode and launch a new Zope instance in debugging mode. Hint: For this purpose the ./docker/.vscode folder contains a prepared VSCode-config file  [launch.json](https://github.com/zms-publishing/ZMS4/blob/main/docker/.vscode/launch.json).

To start the container on the command line, just type: 
```bash
 docker compose run --service-ports zms4  /bin/bash
```
