# Personal Blog
Using Django :shipit:

![Sample of the app](sample.png)

## Poetry
Every time you update the requirements with `poetry add <package>` you need to do (2) `python strip_setuptools.py - && poetry install`.

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
