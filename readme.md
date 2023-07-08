**Odoo Environment**

This is an Odoo environment running version 16.0.

**Requirements** 

Ubuntu 20.04 LTS or later

Python 3.7 or later

PostgreSQL 12 or later

Node.js 14.x or later

Git

**Setup Installation**

Installing linux on virtual machine

checking python3 --version

installing pip3: sudo apt install python3-pip

installing git: sudo apt install git

Adding email to git: git config --global user.email "muhammad.arsalan139@gmail.com"

Adding username to git: git config --global user.name "arsalan139"

Making directory: mkdir programming

Changing path to directory: cd programming

Making subdirectory: mkdir src

Making another subdirectory: mkdir env

Changing path to src subdirectory: cd src

Cloning odoo github repository: git clone https://github.com/odoo/odoo.git

Installing postgresql database: sudo apt install postgresql postgresql-client 

creating postgresql user: sudo -u postgres createuser arsalan

opening postgresql interactive shell: sudo -u postgres psql

creating database: create database arsalan;

Once the Odoo repository has been cloned, we’ll install some more dependencies
sudo apt install python3-pip libldap2-dev libpq-dev libsasl2-dev virtualenv

Return to the programming directory and then cd into env:
$ cd /home/arsalan/programming/
$ cd env/


Now make a Python virtual environment with your project name:
sudo apt install python3-virtualenv
$ virtualenv realestate_management
$ cd ..

Now to activate your virtual environment:
$ source env/realestate_management/bin/activate

Once your virtual environment is activated, install all the packages/libraries you will need for working with Odoo:
$ pip3 install -r src/odoo/requirements.txt

**Addons**
Estate
Estate_Account

**Estate Addon Directory Structure**

Data 
 
Models

Security

Views

__init__.py

__Manifest__.py


**Estate_Account Addon Directory Structure**

__init__.py

__Manifest__.py