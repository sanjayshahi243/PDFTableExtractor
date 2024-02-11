"""
PDFExtractor Application Initialization Module.

This module initializes the PDFExtractor Flask application and sets up necessary components.

Functions:
- celery_init_app(app: Flask) -> Celery: Initialize Celery for the Flask app.
- create_app(test_config=None) -> Flask: Create and configure the Flask app.
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Flask Imports
from flask import Flask

load_dotenv()

from celery import Celery, Task
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()

def celery_init_app(app: Flask) -> Celery:

    """
    Initialize Celery for the Flask app.

    Parameters:
    - app (Flask): The Flask app instance.

    Returns:
    - Celery: The initialized Celery app.
    """

    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app

def create_app(test_config: Optional[dict] = None) -> Flask:

    """
    Create and configure the Flask app.

    Parameters:
    - test_config (dict, optional): Configuration for testing purposes.

    Returns:
    - Flask: The configured Flask app.
    """
     
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY'),
    )
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", 'sqlite:///app.db')

    # Initialize SQLAlchemy
    db.init_app(app)
    migrate.init_app(app, db)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Route imports
    from pdfExtractor.core.routes import core_bp
    
    app.register_blueprint(core_bp)

    from flask import request

    # @app.after_request
    # def after_request(response):
    #     response.status_code = 200
    #     return response

    app.config.from_mapping(
        CELERY=dict(
            broker_url=os.environ.get("BROKER_URL", "redis://localhost:6379/0"),
            result_backend=os.environ.get("RESULT_BACKEND", "redis://localhost:6379/0"),
            task_ignore_result=True,
        ),
    )
    app.config.from_prefixed_env()
    celery_init_app(app)

    from pdfExtractor import models
    return app