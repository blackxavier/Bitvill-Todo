# Bitvill-Contact

## API Endpoints

### Users

* api/register/ - (registers users)
* api/login/ - (logs in users)
* api/logout/ - (logs out users)
* api/change-password/ - (change users password)
* api/me/ - (view users information)

### Todo

* todos/ - (view all todos)
* todos/id/ - (view/edit/update/delete single todo)
* todos/completed/ - (view completed todos)
* todos/archived/ - (view archived todos)

## How to use

### Clone repo

    Clone repository - git clone https://github.com/blackxavier/Bitvill-Todo.git

### Create a virtual environment and install dependencies

    Create a virtual environment - virtualenv env
    Install requirements - pip install -r requirements.txt

### Make migartions and create super user

    Make migrations - py manage.py makemigrations
    Migrate - py manage.py migrate
    Create superuser - py manage.py createsuperuser
    Launch server - py manage.py runserver 
