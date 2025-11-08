set -e

echo "Starting application setup..."

echo "⏳ Waiting for PostgreSQL at $POSTGRES_HOST:$POSTGRES_PORT..."
until python -c "
import sys
import psycopg2
from time import sleep

for i in range(30):
    try:
        conn = psycopg2.connect(
            dbname='$POSTGRES_NAME',
            user='$POSTGRES_USER', 
            password='$POSTGRES_PASSWORD',
            host='$POSTGRES_HOST',
            port='$POSTGRES_PORT'
        )
        conn.close()
        print('PostgreSQL is ready!')
        sys.exit(0)
    except Exception as e:
        if i == 0:
            print('Waiting for PostgreSQL to be ready...')
        sleep(2)

print('PostgreSQL not ready after 60 seconds')
sys.exit(1)
"; do
    sleep 1
done

echo "Applying migrations..."
python manage.py migrate

echo "Checking if database is empty..."
if python manage.py shell -c "
import sys
from django.db import connection

try:
    with connection.cursor() as cursor:
        cursor.execute(\"SELECT to_regclass('api_incident')\")
        table_exists = cursor.fetchone()[0]
        
        if table_exists:
            cursor.execute('SELECT COUNT(*) FROM api_incident')
            count = cursor.fetchone()[0]
            sys.exit(0 if count == 0 else 1)
        else:
            sys.exit(0)
except Exception as e:
    print(f'Error checking database: {e}')
    sys.exit(0)
"; then
    echo "Database is empty, loading fixtures from db.json..."
    
    if [ -f "db.json" ]; then
        if python manage.py loaddata db.json; then
            echo "Fixtures loaded successfully"
        else
            echo "Error loading fixtures, trying alternative approach..."
            python manage.py loaddata db.json --exclude auth.permission --exclude contenttypes --exclude admin.logentry
        fi
    else
        echo "Fixture file db.json not found!"
        exit 1
    fi
else
    echo "Database already has data, skipping fixture load"
fi

echo "Setup completed! Starting server..."
python manage.py runserver 0.0.0.0:8000