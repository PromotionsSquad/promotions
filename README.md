## Markdown for Badges
[![Build Status](https://github.com/PromotionsSquad/promotions/actions/workflows/bdd.yml/badge.svg)](https://github.com/PromotionsSquad/promotions/actions)
[![Build Status](https://github.com/PromotionsSquad/promotions/actions/workflows/tdd.yml/badge.svg)](https://github.com/PromotionsSquad/promotions/actions)
[![codecov](https://codecov.io/gh/PromotionsSquad/promotions/branch/main/graph/badge.svg?token=13A6UGXZDD)](https://codecov.io/gh/PromotionsSquad/promotions)
# Promotions

The promotions resource allows marketing managers to create, read, update, delete, search, and list promotions. At a minimum a promoution should contain a name, a start date, an end date, and whether or not the promotion is active.


## Overview

In this repository you will find the instructions and files for managing promotions. The `/service` folder contains our `models.py` file for our promotions model and a `routes.py` file for promotions. The `/tests` folder has test case starter code for testing the promotions model and the service separately. The functionality of our promotions model will be to create, manage, edit and delete promotions.

## Prerequisite Software Installation

This lab uses Docker and Visual Studio Code with the Remote Containers extension to provide a consistent repeatable disposable development environment for all of the labs in this course.

You will need the following software installed:

Docker Desktop
Visual Studio Code
Remote Containers extension from the Visual Studio Marketplace
All of these can be installed manually by clicking on the links above or you can use a package manager like Homebrew on Mac of Chocolatey on Windows.

Alternately, you can use Vagrant and VirtualBox to create a consistent development environment in a virtual machine (VM).

You can read more about creating these environments in my article: Creating Reproducable Development Environments

## Bring up the development environment

To bring up the development environment you should clone this repo, change into the repo directory:

$ git clone https://github.com/sternie-devops-squad/wishlists.git
$ cd wishlists
Depending on which development environment you created, pick from the following:

# Start developing with Visual Studio Code and Docker

Open Visual Studio Code using the code . command. VS Code will prompt you to reopen in a container and you should say yes. This will take a while as it builds the Docker image and creates a container from it to develop in.

$ code .
Note that there is a period . after the code command. This tells Visual Studio Code to open the editor and load the current folder of files.

Once the environment is loaded you should be placed at a bash prompt in the /app folder inside of the development container. This folder is mounted to the current working directory of your repository on your computer. This means that any file you edit while inside of the /app folder in the container is actually being edited on your computer. You can then commit your changes to git from either inside or outside of the container.

# Using Vagrant and VirtualBox

Bring up the virtual machine using Vagrant.

$ vagrant up
$ vagrant ssh
$ cd /vagrant
This will place you in the virtual machine in the /vagrant folder which has been shared with your computer so that your source files can be edited outside of the VM and run inside of the VM.
