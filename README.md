Recommendation Project
======================


Basic Commands
--------------

### Setting Up Your Users

-   To create a **normal user account**, just go to Sign Up and fill out
    the form. Once you submit it, you'll see a "Verify Your E-mail
    Address" page. Go to your console to see a simulated email
    verification message. Copy the link into your browser. Now the
    user's email should be verified and ready to go.
-   To create an **superuser account**, use this command:

```bash
python manage.py createsuperuser
```

For convenience, you can keep your normal user logged in on Chrome and
your superuser logged in on Firefox (or similar), so that you can see
how the site behaves for both kinds of users.


### Celery

This app comes with Celery.

To run a celery worker:

```bash
cd recommend
celery -A apps.taskapp worker -l info
```
    

Please note: For Celery's import magic to work, it is important *where*
the celery commands are run. If you are in the same folder with
*manage.py*, you should be right.


### Sentry

Sentry is an error logging aggregator service. You can sign up for a
free account at <https://sentry.io/signup/?code=cookiecutter> or
download and host it yourself. The system is setup with reasonable
defaults, including 404 logging and integration with the WSGI
application.

You must set the DSN url in production.


### Installation


```bash
docker-compose -f local.yml build
sudo docker-compose -f local.yml up
```
