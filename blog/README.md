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

## Import CSV
```
docker compose run --rm web python manage.py importcsv csv/Dec_22.csv
```

## Remove duplicate categories from the database
```
from django.db.models import Count, Value
from django.db.models.functions import Trim
from your_app.models import Category  # replace "your_app" with the name of your application

# Group Category objects by trimmed 'name' field and count each group
duplicates = (
    Category.objects
    .annotate(trimmed_name=Trim('name'))
    .values('trimmed_name')
    .annotate(name_count=Count('trimmed_name'))
    .filter(name_count__gt=1)
)

for duplicate in duplicates:
    print(f"Category name: '{duplicate['trimmed_name']}' has {duplicate['name_count']} duplicates.")


# Get the category with PK 5
new_category = Category.objects.get(pk=5)

# Query all transactions with category PK 18
transactions_to_change = Transaction.objects.filter(category__pk=18)

# Update the category to PK 5 for all these transactions
transactions_to_change.update(category=new_category)

# duplicate_category.delete()
```


## Backups
Using cron to backup the db [At 00:00 on Sunday.](https://crontab.guru/once-a-week)
```
0 0 * * 0 docker exec -ti db bash -c "export DATABASE_URL=postgres://postgres:pass@localhost:5432/postgres && pg_dump -O -x ${DATABASE_URL} > '/var/lib/postgresql/data/dump-$(date +%F).sql'"
```
[Digital Ocean documentation](https://www.digitalocean.com/community/tutorials/how-to-use-cron-to-automate-tasks-ubuntu-1804)

## Github Actions
[Building and testing Python, continuous integration (CI) workflow to build and test your Python project.](https://docs.github.com/en/actions/automating-builds-and-tests/building-and-testing-python)

# Contact Me
- contact at enriquetaso dot com
- [LinkedIn](https://www.linkedin.com/in/enriquetaso/)
- [Twitter](https://twitter.com/enriquetaso)

# Reference Links
- [Quickstart: Compose and Django](https://docs.docker.com/samples/django/)
- [Classy Django REST Framework](https://www.cdrf.co/)
- [CKEditor](https://www.codesnail.com/integrating-ckeditor-in-django-admin-and-rendering-html-in-a-template-django-blog-4/)
