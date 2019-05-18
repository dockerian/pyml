# Docker Study
> This page is the note taken for studying Docker



## Content

* [Introduction](#intro)
* [Commands](#comm)



</br><a name="intro"></a>
## Introduction


### Why Docker?
* for developers
  - eliminate virtrual machine problems when working on code together with co-workers
* for operators
  - run and manage apps side by side in isolated containers to get better compute density
* for enterprises
  - build agile software delivery pipelines to ship new features faster more securely and of confidence for both Linex and Windows software

### Features
* Dockers definitions of isolated operating systems are stored as image files
* they are basically a cooking recipe for thins like install Ununtu and then install Apache
* instance of images are called containers
* to make data persistent, we need volumes
* valumes are underlying data layer that we can use for multiple containers
* we hvae networks taht wrap a whole bunch of containers



<br/><a name="comm"></a>
## Commands


## In-Terminal
* run hello-world: create a container with "hello world" image
* ps -a: list containers
* run --name my-hello hello-world: create a container with "hello world" image with name "my-hello"
* run -t --name my-linuc-container ubuntu bash: create a container with "ubuntu" image "my-linuc-container" name bash "command"
* images: list all iamges off-line on my computer
* docker rm $(docker ps -a -f status=exited -q): remove all the container runing
* docker run -it --name my-linux-container --rm -v /Data/Privat/Dokumente/projeckte/Learning/Docker:/my-data ubuntu bash: create a container , with name and image, link it with the local data directory, to the data directory "my-data" in the container, remove the container after exiting
* docker build -t my-ubuntu-image .: build our own image "my-ubuntu-image" with "." refers to the docker file inside the directory (or container)


## In-Dockerfile
* from ubuntu: build container from the public image
* @echo: print
* RUN apt-get upgrade && apt-get undata && apt-get install -y python3: install python3