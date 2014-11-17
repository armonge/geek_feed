# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import

from functools import partial
import threading
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import redis

LISTENERS = []


def redis_listener():
    r = redis.Redis()
    ps = r.pubsub()
    ps.subscribe('geek_feed')
    io_loop = tornado.ioloop.IOLoop.instance()

    for message in ps.listen():
        print(message)
        for element in LISTENERS:
            io_loop.add_callback(partial(element.on_message, message))


class RealtimeHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        LISTENERS.append(self)

    def on_message(self, message):
        self.write_message(message['data'])

    def on_close(self):
        LISTENERS.remove(self)



application = tornado.web.Application([
    (r'/ws/', RealtimeHandler)
])


if __name__ == '__main__':
    threading.Thread(target=redis_listener).start()
    http_server = tornado.httpserver.HTTPServer(application)
    print('Listening on 5001')
    http_server.listen(5001)
    tornado.ioloop.IOLoop.instance().start()
