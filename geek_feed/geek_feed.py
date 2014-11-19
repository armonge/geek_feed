# -*- coding: utf-8 -*-
import os
import json
import datetime

import webapp2
import jinja2

from google.appengine.api import users
from google.appengine.ext import ndb

import models
import utils

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class CleanChannelsPage(webapp2.RequestHandler):
    def get(self):
        channels = models.Channel.query(models.Channel.last_active <= (datetime.datetime.now() - datetime.timedelta(hours=2)))
        for c in channels:
            print c.key.delete()


class EventsPage(webapp2.RequestHandler):
    def get(self, slug):
        events = models.Event.query(ancestor=ndb.Key('Match', slug)).fetch()
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(utils.to_json({
            'events': [event.to_dict() for event in events]
        }))

    def post(self, slug):
        values = json.loads(self.request.body)
        event = models.Event(parent=ndb.Key('Match', slug))
        event.body = values.get('body')
        event.meta = values.get('meta')
        event.put()

        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(utils.to_json(event.to_dict()))


class FeedsListPage(webapp2.RequestHandler):
    def get(self):
        matches = models.Match.query().fetch()
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(utils.to_json({
            'feeds': [match.to_dict() for match in matches]
        }))

    def post(self):
        values = json.loads(self.request.body)
        match = models.Match()
        match.title = values.get('title')
        match.team_a = values.get('team_a')
        match.team_b = values.get('team_b')
        match.put()

        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(utils.to_json(match.to_dict()))


class FeedPage(webapp2.RequestHandler):
    def get(self, slug):
        match = ndb.Key('Match', slug).get()
        if not match:
            self.response.status_int = 404
            return
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(utils.to_json(match.to_dict()))


class MainPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url(self.request.uri))
            return

        token, _ = models.Channel.create_user_channel(user)

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render({
            'token': token,
        }))


application = webapp2.WSGIApplication([
    (r'/channels/clean', CleanChannelsPage),
    (r'/api/feeds/(.*)/events', EventsPage),
    (r'/api/feeds/(.*)', FeedPage),
    (r'/api/feeds', FeedsListPage),
    (r'/.*', MainPage),
], debug=True)
