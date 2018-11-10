
build:
	sudo docker-compose up --no-start --remove-orphans --build

stop:
	docker-compose stop

up:
	docker-compose up --detach

test: up
	docker-compose exec server-backend python /app/manage.py test
	make stop

migrate: up
	docker-compose exec server-backend python /app/manage.py migrate

run: migrate
	docker-compose logs -f
