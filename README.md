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
$ docker-compose run web --rm python manage.py createsuperuser
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

```

## Reference Links
- [Quickstart: Compose and Django](https://docs.docker.com/samples/django/)
- [Classy Django REST Framework](https://www.cdrf.co/)
- [CKEditor](https://www.codesnail.com/integrating-ckeditor-in-django-admin-and-rendering-html-in-a-template-django-blog-4/)
