release: python3 manage.py makemigrations && python3 manage.py migrate
web: bin/start-pgbouncer-stunnel daphne nyunite.asgi:application -p $PORT --bind 0.0.0.0 -v2