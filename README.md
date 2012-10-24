# fixgres

## Postfix config

`sudo fixgres_config domain1.com domain2.com`

You'll need to setup postfix to accept all mail from all domains that have MX records pointing to your server. This creates empty directories for each domain in `/var/mail` writes `/etc/postfix/virtual` and `/etc/postfix/main.cf`, `postmap`s the `virtual` file, and reloads the `postfix` service.

## Postgres config

`dropdb fixgres; createdb fixgres && psql fixgres < schema.sql`

## Python config

`python setup.py develop` or `install`, whatever.

## Running

Add `fixgres_work` to your cron or something.
