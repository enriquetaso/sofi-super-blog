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

---

## Deploy
Currently, I have my blog deployed with [Render](https://render.com/) + poetry.

I've followed this [outdated guide](https://render.com/docs/deploy-django#update-your-app-for-render). Then are some stuff to keep an eye on when working with new Django versions.

1. Set an env var `PYTHON ENV` to python 3.10 or something like that.
2. You may have a [setuptools error](https://community.render.com/t/build-can-not-execute-setup-py-since-setuptools-is-not-available/5004). If you are using poetry 1.2.x locally, you will get a build error on Render since the default version is 1.1.x. As a workaround the reporter of the bug created a gist that fixes compatibility of the .lock file (it removes the setup tools elements), Hence, using the following build command:
```
 python strip_setuptools.py - && poetry install
```
3. If you're using the free account you will need to define the Django superuser with environment variables `DJANGO_SUPERUSER_PASSWORD`, `DJANGO_SUPERUSER_EMAIL` and `DJANGO_SUPERUSER_USERNAME`. Check to `build.sh` file.
4. I've also [configured Cloudflare DNS](https://render.com/docs/configure-cloudflare-dns), if you are not familiar with this configuration remember to remove all the `A`.


## Reference Links
- [Quickstart: Compose and Django](https://docs.docker.com/samples/django/)
- [Classy Django REST Framework](https://www.cdrf.co/)
- [CKEditor](https://www.codesnail.com/integrating-ckeditor-in-django-admin-and-rendering-html-in-a-template-django-blog-4/)
