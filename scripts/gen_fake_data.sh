#!bin/bash

if [ -z "$1" ]; then
  echo "Error, provide amount of users and textbooks to generate."
  exit 1
fi

count="$1"

uv run python ../textbook_marketplace/manage.py generate_fake_users $count
uv run python ../textbook_marketplace/manage.py generate_fake_textbooks $count