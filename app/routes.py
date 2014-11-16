# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import

import flask
from flask import g, session, request, redirect, render_template, flash, url_for
from . import app
from . import models

from flask.ext.openid import OpenID
oid = OpenID(app, '/tmp', safe_roots=[])

@app.route('/api/feeds')
def feeds_list():
    matches = models.get_matches()
    return flask.jsonify({
        'feeds': matches
    })


@app.route('/api/feeds/<slug>')
def feed_detail(slug):
    match = models.get_match(slug)
    return flask.jsonify(match)


@app.route('/')
def root():
    return render_template('index.html')


@app.before_request
def lookup_current_user():
    g.user = None
    if 'openid' in session:
        openid = session['openid']
        g.user = models.get_user(openid)


@app.route('/login', methods=['GET', 'POST'])
@oid.loginhandler
def login():
    if g.user is not None:
        return redirect(oid.get_next_url())
    if request.method == 'POST':
        openid = request.form.get('openid')
        if openid:
            return oid.try_login(openid, ask_for=['email', 'nickname'],
                                         ask_for_optional=['fullname'])

    return render_template('login.html', next=oid.get_next_url(),
                           error=oid.fetch_error())



@oid.after_login
def create_or_login(resp):
    session['openid'] = resp.identity_url
    user = models.get_user(resp.identity_url)
    if user is not None:
        flash(u'Successfully signed in')
        g.user = user
        return redirect(oid.get_next_url())
    return redirect(url_for('create_profile', next=oid.get_next_url(),
                            name=resp.fullname or resp.nickname,
                            email=resp.email))


@app.route('/create-profile', methods=['GET', 'POST'])
def create_profile():
    if g.user is not None or 'openid' not in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        if not name:
            flash(u'Error: you have to provide a name')
        elif '@' not in email:
            flash(u'Error: you have to enter a valid email address')
        else:
            flash(u'Profile successfully created')

            models.set_user(session['openid'], {
                'name': name,
                'email': email
            })
            return redirect(oid.get_next_url())

    return render_template('create_profile.html', next=oid.get_next_url())
