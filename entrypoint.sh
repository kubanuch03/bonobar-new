apt install redis-server
redis-server --port 6379 &

sleep 6

python manage.py migrate --noinput
python manage.py collectstatic --noinput
gunicorn bono_bar.wsgi:application --bind 0.0.0.0:8000  --workers 4 --timeout 60

celery -A bono_bar worker --loglevel=info --detach

celery -A bono_bar beat --loglevel=info --detach

wait -n
