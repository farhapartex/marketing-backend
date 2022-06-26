## Digitla Marketing Backend


### Docker commands
* docker-compose exec web python manage.py migrate
* docker-compose exec web python manage.py shell


### Celery commands

* celery -A core worker -l info
* celery -A core beat -l info