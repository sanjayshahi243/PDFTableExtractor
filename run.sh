#! /bin/bash

# Deactivate any existing virtual environment
source deactivate

# Create a virtual environment
python3 -m venv virtualenv
source virtualenv/bin/activate

# Install requirements
pip install -r requirements/local.txt

# Migrate Models
flask db upgrade

# Run Celery worker in the background
celery -A pdfExtractor.make_celery worker -l INFO &

# Run Flower in the background
celery -A pdfExtractor.make_celery -b "${BROKER_URL}" flower &

# Run Flask in the background
flask run --no-reload --no-debug &
