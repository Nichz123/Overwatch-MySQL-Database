# MySQL Database
This web app connects to a local database made using MySQL WorkBench filled generates tables for the user to query revelent information regardng the characters.

## Installation
Assuming python is installed, install the following modules:
```
pip install flask
pip install mysql-connector-python
```
After creating a MySQL Wrokbench database connect it by creating a .env with the following information:
```
MYSQL_USERNAME = WOUR_USERNAME
MYSQL_PASSWORD = YOUR_PASSWORD
MYSQL_PORT = YOUR_PORT
MYSQL_DATABASE = YOUR_DATABASE
```
Replace YOUR_* fields with the relevant info.