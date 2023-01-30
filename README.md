# Personal Blog
Using Django :shipit:

![Sample of the app](sample.png)

## Run To Do App
This project uses `docker` and `docker-compose`.

First, built the image
```
$ docker-compose build
```

Second, synchronise your database for the first time
```
$ docker-compose run --rm web python manage.py migrate
```

Then, create a superuser
```
$ docker-compose run --rm web python manage.py createsuperuser
```

Finally, start the web server. 
```
$ docker-compose up
```
Now you will see the starting development server at `localhost:8000/`.

To remove all containers run
```
$ docker-compose down
```


## Run Test

```
$ docker-compose run --rm web python manage.py test

```
## Dependencies
```
sudo apt install postgresql-client-common
```

## Backups
Using cron to backup the db [At 00:00 on Sunday.](https://crontab.guru/once-a-week)
```
0 0 * * 0 docker exec -ti db bash -c "export DATABASE_URL=postgres://postgres:pass@localhost:5432/postgres && pg_dump -O -x ${DATABASE_URL} > '/var/lib/postgresql/data/dump-$(date +%F).sql'"
```
[Digital Ocean documentation](https://www.digitalocean.com/community/tutorials/how-to-use-cron-to-automate-tasks-ubuntu-1804)

## Github Actions
[Building and testing Python, continuous integration (CI) workflow to build and test your Python project.](https://docs.github.com/en/actions/automating-builds-and-tests/building-and-testing-python)

# Reference Links
- [Quickstart: Compose and Django](https://docs.docker.com/samples/django/)
- [Classy Django REST Framework](https://www.cdrf.co/)
- [CKEditor](https://www.codesnail.com/integrating-ckeditor-in-django-admin-and-rendering-html-in-a-template-django-blog-4/)
