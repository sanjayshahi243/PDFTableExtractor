"""
PDFExtractor Celery Configuration Module.

This module configures and initializes Celery for the PDFExtractor Flask application.

Functions:
- make_celery(app) -> Celery: Create and configure Celery for the Flask app.
"""

from pdfExtractor import create_app

flask_app = create_app()
celery_app = flask_app.extensions["celery"]
