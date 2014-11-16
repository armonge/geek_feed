# -*- coding: utf-8 -*-
import datetime

import flask
from flask import Flask

from flask.ext.login import LoginManager

class GeekFeedJSONEncoder(flask.json.JSONEncoder):
    def default(self, o):
        print(o)
        if isinstance(o, datetime.datetime):
            return o.strftime('%s')

        return super(GeekFeedJSONEncoder, self).default(o)

app = Flask(__name__, static_url_path='')
flask.json.JSONEncoder = GeekFeedJSONEncoder
app.config.from_object('config')
login_manager = LoginManager()
login_manager.init_app(app)

from app import models
from app import routes
