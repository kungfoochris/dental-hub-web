Dental Hub
===========
To run with docker

1. To build docker `docker-compose build`
2. To run docker `docker-composer up`
3. To access shell `docker exec -it container_id bash`
4. To shutdown docker containers `docker-composer down`

To run with virtualenv

1. To create a virtualenv `pip install virtualenv`
2. To activate virtualenv `workon <env_name>`
3. To install requirements `pip install -r requirements/<requirement_name>`
4. To run the system  `python manage.py runserver`