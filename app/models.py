import redis
import datetime
from flask import json
from slugify import slugify
from . import app
from .utils import Event
from .listeners import push_event_created_notification, push_match_created_notification

r_server = redis.Redis.from_url(app.config['REDIS_URL'])

matches_set_key = 'matches'
match_mask = 'match:{slug}'
events_set_mask = 'match:{slug}:events'
event_mask = 'event:{id}'
event_counter_key = 'events'

match_created = Event()
event_created = Event()

match_created.append(push_match_created_notification)
event_created.append(push_event_created_notification)


def create_match(match):
    match['slug'] = match.get('slug', slugify(match['title']))
    match['timestamp'] = match.get('timestamp', datetime.datetime.now().strftime('%s'))

    match_key = match_mask.format(**match)
    pipe = r_server.pipeline()
    pipe.set(match_key, json.dumps(match))
    pipe.zadd(matches_set_key, match['slug'], match['timestamp'])

    match_created(match)
    return match, pipe.execute()


def get_match(slug):
    match_key = match_mask.format(slug=slug)
    match = json.loads(r_server.get(match_key))
    return match


def get_match_events(slug):
    events_set = r_server.zrange(events_set_mask.format(slug=slug), 0, -1)
    pipe = r_server.pipeline()
    for event_id in events_set:
        pipe.get(event_mask.format(id=event_id))

    events = [json.loads(event) for event in pipe.execute()]

    return events


def get_matches():
    slug_set = r_server.zrange(matches_set_key, 0, -1)
    pipe = r_server.pipeline()
    for slug in slug_set:
        pipe.get(match_mask.format(slug=slug))

    return [json.loads(match) for match in pipe.execute()]


def create_event(match_slug, event):
    event_id = r_server.incr(event_counter_key)
    event['id'] = event_id
    event['timestamp'] = event.get('timestamp', datetime.datetime.now().strftime('%s'))

    pipe = r_server.pipeline()

    pipe.zadd(events_set_mask.format(slug=match_slug), event_id, event['timestamp'])
    pipe.set(event_mask.format(id=event_id), json.dumps(event))

    event_created(match_slug, event)
    return event, pipe.execute()
