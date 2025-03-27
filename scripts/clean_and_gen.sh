#!/bin/bash

: '
This script runs both rm_db_data.sh and gen_fake_data.sh scripts, for more
information read docs inside them.

Usage example:

bash clean_and_gen.sh 5
'
SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"

if [ -z "$1" ]; then
  echo "Error, provide amount of users and textbooks to generate."
  exit 1
fi

count="$1"
echo "Running script to delete data from db..."
source "$SCRIPT_DIR/rm_db_data.sh"

echo "Running script to generate new fake users and textbooks to db..."
source "$SCRIPT_DIR/gen_fake_data.sh" "$count"
