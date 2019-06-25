#!/bin/bash
# wait-for-db.sh

set -e

host="$1"
shift
cmd="$@"
echo "Something is fishy here."
export PGPASSWORD="some_strong_password"
until psql -h "$host" -U "postgres" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - executing command"
exec $cmd

