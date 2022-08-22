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
$ docker-compose run --rm python manage.py migrate
```

Then, create a superuser
```
$ docker-compose run --rm python manage.py createsuperuser
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
$ docker-compose run --rm python manage.py test

Creating radiologists_notebook_web_run ... done
Found 1 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
.
----------------------------------------------------------------------
Ran 1 test in 0.198s

OK
Destroying test database for alias 'default'...
```

## Reference Links
- [Quickstart: Compose and Django](https://docs.docker.com/samples/django/)
- [Classy Django REST Framework](https://www.cdrf.co/)
