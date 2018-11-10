stop:
	docker-compose stop

up:
	docker-compose up --detach

test: up
	docker-compose exec server-backend python /app/manage.py test

migrate: up
	docker-compose exec server-backend python /app/manage.py migrate

run: migrate
	docker-compose logs -f
