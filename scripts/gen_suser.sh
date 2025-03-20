#!/bin/bash/expect -f

: '
!Git Bash required!
This script helps create superuser to get access to django admin panel.
Credentials are taken from .env file:
username - root
email - root@example.com

You only need to input password and repeat it to create superuser.
'
SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"

uv run winpty python "$SCRIPT_DIR/../textbook_marketplace/manage.py" createsuperuser --username "root" --email "root@example.com"
