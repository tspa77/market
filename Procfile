release: python django_site/manage.py migrate 
web: gunicorn django_site.wsgi --chdir ./django_site --log-file -