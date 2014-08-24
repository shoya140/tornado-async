# coding:UTF-8

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.httpclient
import tornado.gen

import urllib
from key import config

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)
define("debug", default=False, help="autoreload during debug is true", type=bool)

class IndexHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
        query = self.get_argument("q", u"hello, world").encode("utf-8")
        client = tornado.httpclient.AsyncHTTPClient()
        response = yield tornado.gen.Task(client.fetch,
            "http://jlp.yahooapis.jp/KeyphraseService/V1/extract?" + \
            urllib.urlencode({"appid":config.Yahoo.app_id,
            "sentence": query, "output":"json"}))
        body = json.loads(response.body)
        if body:
            self.write(body)
        self.finish()

if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers = [(r"/",  IndexHandler)], debug = options.debug)
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
