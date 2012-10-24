# Resources:

The files below all come from James A. Woods, web2
(Webster's Second International):

    corpora/bigrams
    corpora/connectives
    corpora/propernames
    corpora/unigrams

---

# Step 0:

## `bootstrap.py`

You'll want to get the database all set up. Run `bootstrap.py` without any
arguments as a user who can create a database, and who should own the
`mailmaster` database.

## `sudo write_postfix_config`

You'll also need to setup postfix to accept all mail from all domains in
the `data/domains` file, which should have all their MX records pointing to
this server. Also writes `/etc/postfix/virtual` and `/etc/postfix/main.cf`
`postmap`s the `virtual` file, and reloads the `postfix` service.

---

# Step 1:
## `create_account.py` & (`create_account.js`)

### running condition:  continuous
### stopping condition: 1000 unregistered accounts available

Generate name, ensure it doesn't exist on twitter, pick email, password, add
to database (marked as created, by default).

---

# Step 2:
## `register_account.py`

### running condition:  continuous
### stopping condition: no accounts unregistered

Create account on Twitter, mark it as "registered" in the database.

---

# Step 3:
## `confirm_account.py`

### running condition:  continuous
### stopping condition: no accounts unconfirmed

---

# Development

The python bottle app is serving on :5051
Nginx should listen on :5050

## Web UI

using htpasswd.py:

    htpasswd.py -c -b nginx.htpasswd username password

### Supervisor (/etc/supervisor/conf.d/updown.in):

    [program:updown.in]
    directory=/www/mailmaster
    command=python mailmasterui.py
    autorestart=true
    user=chbrown

### Nginx (/etc/nginx/sites-enabled):

    server {
        listen 5050;
        server_name updown.in *.updown.in;

        location ~ ^/(css|img|js) {
            root /www/mailmaster/static;
        }
        location /templates {
            root /www/mailmaster;
        }
        location / {
            auth_basic "Restricted";
            auth_basic_user_file  /www/mailmaster/nginx.htpasswd;

            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Host $host;
            proxy_pass http://127.0.0.1:5051;
            proxy_redirect default;
        }
    }
