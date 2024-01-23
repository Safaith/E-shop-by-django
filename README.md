# E-commerce

This is a very simple e-commerce website built with django 

## Features

* This project has user authentication and authorization
* An annonymous  user can cart products by cookies. Before transaction, There will need personal information. Based on his/her personal info, there will create an user in user-field.  
* Shipping form for shipping objects


## Running this project

To get this project up and running you should start by having python installed on your computer.It's advised you create a virtual environment to store your projects dependencies separately.You can install virtualenv with 

```
pip install virtualenv
```
Clone or download this repository and open it in your editor of choice. In a terminal (mac/linux) or windows terminal, run the following command in the base directory of this project

```
virtualenv env
```
That will create a new folder `env` in your project directory. Next activate it with this command on mac/linux:

```
source env/bin/activate
```
Then install the project dependencies with

```
pip install -r requirements.txt
```
Now you can run the project with this command

```
python manage.py runserver
```