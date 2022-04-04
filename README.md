## Markdown for Badges

### Find Commands Below 

[![Build Status](https://github.com/PromotionsSqaud/promotions/actions/workflows/tdd.yml/badge.svg)](https://github.com/PromotionsSquad/promotions/actions)

# Promotions

Below are the instructions for creating and managing promotions

You can find more information below.



## Overview

In this repository you will find the instructions and files for managing promotions. The `/service` folder contains our `models.py` file for our promotions model and a `routes.py` file for promotions. The `/tests` folder has test case starter code for testing the promotions model and the service separately. The functionality of our promotions model will be to create, manage, edit and delete promotions.

## Contents

Our promotions project contains the following:

```text
.coveragerc         - settings file for code coverage options
.devcontainers      - support for VSCode Remote Containers
.gitignore          - this will ignore vagrant and other metadata files
dot-env-example     - copy to .env to use environment variables
requirements.txt    - list if Python libraries required by your code
config.py           - configuration parameters

service/                - service python package
├── __init__.py         - package initializer
├── error_handlers.py   - HTTP error handling code
├── models.py           - module with business models
├── routes.py           - module with service routes
└── status.py           - HTTP status constants

tests/              - test cases package
├── __init__.py     - package initializer
├── test_models.py  - test suite for business models
└── test_routes.py  - test suite for service routes

Vagrantfile         - sample Vagrant file that installs Python 3 and PostgreSQL
``
