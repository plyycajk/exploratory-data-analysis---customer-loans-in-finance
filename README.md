# exploratory-data-analysis---customer-loans-in-finance

## Contents
1. [Description](#description)
1. [Installation instructions](#installation-instructions)
1. [Usage instructions](#usage-instructions)
1. [File structure](#file-structure)
1. [License information](#license-information)

## Description
This project accesses a relational database and extracts data for exploratory data analysis.

I learnt how to use SQLAlchemy to connect to a database as well as how to structure this within a class by use of the  __ enter __ and __ exit __ magic methods.

I also learnt how to keep login details out of scripts by use of the separate .yaml file in the directory, and using .gitignore to prevent this information being shared to the Github repository.

## Installation instructions

This project requires the following packages to be installed in order to run correctly:

- pandas
- SQLAlchemy
- Pyyaml

In order to establish a connection to the database, db_utils. py requires a .yaml file (with database connection credentials) to be saved in the same directory. Values need to be populated against the following keys:

- RDS_HOST: {link/id for the database}
- RDS_PASSWORD: {password for the user to access the  database}
- RDS_USER: {username for the user to access the  database} 
- RDS_DATABASE: {name of database}
- RDS_PORT: {port to be accessed}

## Usage instructions

A yaml file with database log-in credentials is required in order to establish the database. This should be stored in the same directory as the scripts.
- running db_utils.py as a script will require this file to be called 'credentials.yaml'. The class is written in such a way to allow any named yaml file to be called when the class is imported as a module

## File structure

### db_utils.py

This file initiates a class (RDSDatabaseConnector) which establishes a connection with the database. 
Subsequent functions in this file run a specific query in the database to extract loan patyment information and save this to a .csv file (loan_payments.csv).


## License information
None