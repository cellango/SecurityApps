#!/bin/bash
# wait-for-it.sh

set -e

host=$(echo "$1" | cut -d: -f1)
shift
cmd="$@"

echo "Debug: Host is $host"
echo "Debug: Command is $cmd"
echo "Debug: Current directory is $(pwd)"
echo "Debug: Environment variables:"
env | grep PG

until PGPASSWORD=postgres psql -h "$host" -U "postgres" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - executing command"
exec $cmd
