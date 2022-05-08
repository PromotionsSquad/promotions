## Markdown for Badges
[![Build Status](https://github.com/PromotionsSquad/promotions/actions/workflows/bdd.yml/badge.svg)](https://github.com/PromotionsSquad/promotions/actions)
[![Build Status](https://github.com/PromotionsSquad/promotions/actions/workflows/tdd.yml/badge.svg)](https://github.com/PromotionsSquad/promotions/actions)
[![codecov](https://codecov.io/gh/PromotionsSquad/promotions/branch/main/graph/badge.svg?token=13A6UGXZDD)](https://codecov.io/gh/PromotionsSquad/promotions)
# Promotions

The promotions resource allows marketing managers to create, read, update, delete, search, and list promotions. At a minimum a promoution should contain a name, a start date, an end date, and whether or not the promotion is active.

## Prerequisite Software Installation

This lab uses Docker and Visual Studio Code with the Remote Containers extension to provide a consistent repeatable disposable development environment for all of the labs in this course.

You will need the following software installed:

[Docker Desktop](https://www.docker.com/products/docker-desktop/)

[Visual Studio Code](https://code.visualstudio.com/)

[Remote Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) extension from the Visual Studio Marketplace

All of these can be installed manually by clicking on the links above or you can use a package manager like Homebrew on Mac of Chocolatey on Windows.

Alternately, you can use Vagrant and VirtualBox to create a consistent development environment in a virtual machine (VM).

You can read more about creating these environments in John Rofrano's article: [Creating Reproducable Development Environments](https://medium.com/nerd-for-tech/creating-reproducible-development-environments-fac8d6471f35)

## Bring up the development environment

1. Navigate to DevOps Folder
2. Clone the Repo

```
$ git clone https://github.com/sternie-devops-squad/wishlists.git
```

3. Change directory to promotions:

```
$ cd promotions
```

4. Open Visual Studio Code using the code . command. VS Code will prompt you to reopen in a container and you should say yes. This will take a while as it builds the Docker image and creates a container from it to develop in.

```
$ code .
```
Note that there is a period `.` after the `code` command. This tells Visual Studio Code to open the editor and load the current folder of files.

5. Open in Container - Make sure docker is running or you won't be able to open in container
6. Pull up-to-date code from GitHub

```
$ git pull
```

## Running Nosetests

As developers we always want to run the tests before we change any code. That way we know if we broke the code or if someone before us did. Always run the test cases first!

1. Run the tests using `nosetests`

```
$ nosetests
```
## Accessing WebUI and Running BDD Tests

1. The project uses honcho which gets it's commands from the Procfile. To start the service simply use:

```
$ honcho start
```
You should be able to reach the service at: http://localhost:8080. The port that is used is controlled by an environment variable defined in the .flaskenv file which Flask uses to load it's configuration from the environment by default.

Once in the environment try various actions such as:
- Add a new promotion
- Update an existing promotion
- Delete an existing promotion
- Search for promotions
- Query promotions by active status

2. Run behave tests

```
$ behave
```

