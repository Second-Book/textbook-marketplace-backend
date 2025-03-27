#!/bin/bash

: '
This script runs django backend server.
'

SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"

uv run python "$SCRIPT_DIR/../textbook_marketplace/manage.py" runserver