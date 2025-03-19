#!/bin/bash/expect -f

: '
!Git Bash required!
This script helps create superuser to get access to django admin panel.
Credentials are taken from .env file:
username - $DB_USER
email - $DB_USER@example.com

You only need to input password and repeat it to create superuser.
'
SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"

env_path="$SCRIPT_DIR/../.env"

if [ -f "$env_path" ]; then
  source "$env_path"
else
  echo "No .env file in project root."
  exit 1
fi

uv run winpty python "$SCRIPT_DIR/../textbook_marketplace/manage.py" createsuperuser --username "$DB_USER" --email "$DB_USER@example.com"
