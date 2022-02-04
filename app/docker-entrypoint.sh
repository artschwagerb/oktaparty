#!/bin/sh
set -e

# until psql $DATABASE_URL -c '\l'; do
#     >&2 echo "Postgres is unavailable - sleeping"
#     sleep 1
# done

if [ "$DJANGO_MANAGEPY_MIGRATE" = '1' ]; then
    python manage.py migrate --noinput
fi

if [ "$DJANGO_MANAGEPY_COLLECTSTATIC" = '1' ]; then
    python manage.py collectstatic --noinput
fi

exec "$@"