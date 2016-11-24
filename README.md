## Development

### Initial setup

You need Python, virtualenv and Postgres.

Start the DB:

    mkdir -p tmp/postgres
    initdb tmp/postgres
    postgres -D tmp/postgres -p 5432

Create the initial DB (in another tab):

    psql postgres -p 5432 -c "create user zagrad with password 'zagrad';"
    psql postgres -p 5432 -c "create database zagrad encoding 'utf8' template template0 owner zagrad;"

Get Python dependencies:

    virtualenv venv
    ./venv/bin/activate
    pip install -r requirements.txt

Copy and if necessary edit your *local.py*

    cp votify/settings/local.example.py votify/settings/local.py

Initial DB setup for Python:

    python manage.py syncdb

Run migrations:

    python manage.py migrate

Create the site:

    python manage.py shell
    >>> from django.contrib.sites.models import Site
    >>> Site.objects.create(name='localhost', domain='localhost')
    >>> quit()

You can now close both tabs (the postgres process too).

Copy and if necessary edit your *Procfile.dev*

    cp Procfile.dev.example Procfile.dev

### Normal workflow

Run any migrations (if neccessary) and start both the DB and the server:

    honcho -f Procfile.dev start

If you only want to start the development server:

    python manage.py runserver

In this case the DB needs to be running separately with:

    postgres -D tmp/postgres -p 5432
