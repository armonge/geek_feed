# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import

from utils import send


def push_event_created_notification(match_slug, event, **kwargs):
    send('new-event:{slug}'.format(slug=match_slug), event.to_dict())


def push_match_created_notification(match, **kwargs):
    send('new-feed', match.to_dict())
