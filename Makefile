shell:
	docker-compose run --rm web /bin/sh

superuser:
	docker-compose run --rm web python manage.py createsuperuser

makemigrations:
	docker-compose run --rm web python manage.py makemigrations

migrate:
	docker-compose run --rm web python manage.py migrate