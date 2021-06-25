#!/usr/bin/env bash

function create_container(){
    codebase_dir=$(realpath $1)

    if [ $# -lt 1 ]; then
        echo "Please provide the file directory to the codebase you wish to document."
        exit 1
    fi

    if [ ! -d "$codebase_dir" ]; then
      echo "$codebase_dir does not exist"
      exit 1
    fi

    docker run -it \
    --name dbs_autodoc_con \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -v $(pwd):/home/qtuser/dbs_autodoc:Z \
    -v $codebase_dir:/home/qtuser/codebase-to-doc:Z \
    -e DISPLAY=$DISPLAY \
    -u qtuser \
    -w /home/qtuser/dbs_autodoc \
    dbs_autodoc_image bash
}

# Check if Docker is installed.
# If not installed, install it.
if output=$(docker --version > /dev/null 2>&1); then
    :
else
    echo "Installing Docker..."
    echo "Reference: [ https://docs.docker.com/engine/install/ubuntu/ ]"
    sudo apt-get remove -y docker \
      docker-engine \
      docker.io \
      containerd \
      runc
    sudo apt-get update && \
    sudo apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    sudo add-apt-repository \
    "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
    $(lsb_release -cs) \
    stable"
    sudo apt-get update
    sudo apt-get install -y docker-ce \
      docker-ce-cli \
      containerd.io
fi

echo "Docker [ FOUND ]"

# Check if dbs_autodoc_image has been created from Dockerfile.
# If not created, create it.
if output=$(docker images | grep dbs_autodoc_image > /dev/null 2>&1); then
    :
else
    docker build --tag dbs_autodoc_image .
fi

echo "dbs_autodoc_image Docker Image [ FOUND ]"

# Check if dbs_autodoc_container has been created from image.
# If not created, create it and run it.
if output=$(docker ps -a | grep dbs_autodoc_con > /dev/null 2>&1); then
    echo "Existing dbs_autodoc_con Docker Container [ FOUND ]"
    read -p "Do you wish to overwrite? [y/n]" input

    if [[ $input == "y" ]]; then
        docker stop dbs_autodoc_con >/dev/null 2>&1
        docker rm dbs_autodoc_con >/dev/null 2>&1
        create_container $1
    elif [[ $input == "n" ]]; then
        docker start dbs_autodoc_con >/dev/null 2>&1
        docker exec -it dbs_autodoc_con bash
    fi

else
    create_container $1
fi

unset output input codebase_dir
