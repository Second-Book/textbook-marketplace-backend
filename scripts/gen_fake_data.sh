#!/bin/bash

: '
This script creates fake users and fake textbooks. The amount of created units
depends on provided argument.

Usage example:
bash gen_fake_data.sh 5
'

if [ -z "$1" ]; then
  echo "Error, provide amount of users and textbooks to generate."
  exit 1
fi

count="$1"

echo "Generating fake users..."
uv run python ../textbook_marketplace/manage.py generate_fake_users $count

echo "Generating fake textbooks..."
uv run python ../textbook_marketplace/manage.py generate_fake_textbooks $count