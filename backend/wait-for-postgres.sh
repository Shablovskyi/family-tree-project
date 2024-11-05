#!/bin/bash
# wait-for-postgres.sh

set -e

host="$1"
shift
cmd="$@"

# Використовуємо змінну середовища PGPASSWORD для пароля
export PGPASSWORD="$POSTGRES_PASSWORD"

until psql -h "$host" -U "$POSTGRES_USER" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - executing command"
exec $cmd