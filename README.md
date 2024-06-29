# Shop with items in Django
It is test version.
This is project for Studying in WSB Merito

database in sqlite

session is saving in cookies.



## Installation

Download, add virtual env

install requirements.txt

go into path with manage.py

python manage.py createsuperuser, 
answer options and create admin user.

python mange.py makemigrations

python manage.py migrate

to enable sqlite

python manage.py runserver
to start server

You are ready to test it out.

```

## Usage

First create Size
Second create Category
Third create Product

ProductSizes will create by themselfs.
Just edit them to set availability.

Users can create accounts, they have to give an email for which they will obtain a activation account link.
User can forgot password, and recovery it by using their email.

Payment is working with paypal. It was tested only at sand accounts yet.
Blik payment is best for tests.

```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.
Please make sure to update tests as appropriate.

### GOAL OF PROJECT

The goal of the project is to create an e-commerce template with various items, so that it can serve as a foundation for easily setting up a store for small sellers :)

Ultimately, users won't need programming skills to customize the store to their needs.

