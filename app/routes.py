# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import

from flask import render_template, request, jsonify
from . import app
from . import models


@app.route('/api/feeds', methods=['GET'])
def feeds_list():
    matches = models.get_matches()
    return jsonify({
        'feeds': matches
    })


@app.route('/api/feeds', methods=['POST'])
def create_feed():
    match, log = models.create_match(request.json)
    return jsonify({'feed': match, 'log': log})


@app.route('/api/feeds/<slug>')
def feed_detail(slug):
    match = models.get_match(slug)
    return jsonify(match)


@app.route('/api/feeds/<slug>/events', methods=['GET'])
def feed_events(slug):
    match_events = models.get_match_events(slug)
    return jsonify({'events': match_events})


@app.route('/api/feeds/<slug>/events', methods=['POST'])
def push_feed_event(slug):
    event, log = models.create_event(slug, request.json)
    return jsonify({'event': event, 'log': log})


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def root(path):
    print(path)
    return render_template('index.html')
