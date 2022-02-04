shell:
	docker-compose run --rm web /bin/sh

superuser:
	docker-compose run --rm web python manage.py createsuperuser