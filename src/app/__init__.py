from flask import Flask
from flask_restplus import Api

from .config import config

app = Flask(__name__)

app.config.from_object(config['default'])
api = Api(app,
          # doc='/swagger',
          version='0.1.2',
          title='SSkey',
          description='A simple application to safe yours passwords')

from . import routes
