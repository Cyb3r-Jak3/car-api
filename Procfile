web: gunicorn -k gevent --preload --workers 8 app:app
release: flask db upgrade
worker: python worker.py