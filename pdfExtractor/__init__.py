import os
from dotenv import load_dotenv

# Flask Imports
from flask import Flask

# load_dotenv()

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY'),
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    
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
    return app