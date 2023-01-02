build:
	docker compose build
start:
	docker compose up -d

collecstatic:
	docker compose run --rm web	python manage.py collectstatic

shell:
	docker compose run --rm web bash

python:
	docker compose run --rm web	python manage.py shell_plus

clean:
	docker compose down

remove:
	docker compose down -v 

migrate:
	docker compose run --rm web python manage.py migrate

start-db:
	docker compose up -d db && docker compose logs -f db

get-dumped:
    # export DATABASE_URL=postgres://postgres:pass@localhost:5432/postgres
	pg_dump -O -x ${DATABASE_URL} > "dump-$(date +%F).sql"