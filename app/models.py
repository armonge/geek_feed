import redis
from flask import json
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
    match_key = match_mask.format(**match)
    pipe = r_server.pipeline()
    pipe.set(match_key, json.dumps(match))
    pipe.zadd(matches_set_key, match['slug'], match['timestamp'])

    return pipe.execute()


def get_match(slug):
    match_key = match_mask.format(slug=slug)
    match = json.loads(r_server.get(match_key))
    events_set = r_server.zrange(events_set_mask.format(slug=slug), -1, -1)

    pipe = r_server.pipeline()
    for event_id in events_set:
        pipe.get(event_mask.format(id=event_id))

    events = [json.loads(event) for event in pipe.execute()]

    match['events'] = events
    return match


def get_matches():
    slug_set = r_server.zrange(matches_set_key, -1, -1)
    pipe = r_server.pipeline()
    for slug in slug_set:
        pipe.get(match_mask.format(slug=slug))

    return [json.loads(match) for match in pipe.execute()]


def create_event(match_slug, event):
    event_id = r_server.incr(event_counter_key)
    pipe = r_server.pipeline()

    pipe.zadd(events_set_mask.format(slug=match_slug), event_id, event['timestamp'])
    pipe.set(event_mask.format(id=event_id), json.dumps(event))

    return pipe.execute()


def set_user(token):
    r_server.set('user:{token}'.format(token=token), json.dumps({}))


def get_user(open_idj):
    return json.loads(r_server.get('user:{id}'.format(id=open_id)))
