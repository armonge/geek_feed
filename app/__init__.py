# -*- coding: utf-8 -*-
import datetime

import redis
import flask
from flask import Flask


class GeekFeedJSONEncoder(flask.json.JSONEncoder):
    def default(self, o):
        print(o)
        if isinstance(o, datetime.datetime):
            return o.strftime('%s')

        return super(GeekFeedJSONEncoder, self).default(o)


app = Flask(__name__, static_url_path='')
flask.json.JSONEncoder = GeekFeedJSONEncoder
app.config.from_object('config')
r_server = redis.Redis.from_url(app.config['REDIS_URL'])

from app import models
from app import routes

