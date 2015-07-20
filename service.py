#!/usr/bin/env python

__author__ = 'litrin.jiang@intel.com'

import os

import tornado.ioloop
import tornado.web
import tornado.httpclient
from tornado.options import define, options, parse_command_line

define("api_url", default="http://10.239.163.50:888", help="api url")
define("port", default="80", help="service port")
define("debug", default="", help="debug mode")
define("pid_file", default="api2api.pid", help="pid file")

class SwitchOperation(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        http_client = tornado.httpclient.AsyncHTTPClient()
        http_client.fetch(self.get_url(), callback=self.on_fetch)

    @tornado.web.asynchronous
    def post(self):
        a = self.request.body
        http_client = tornado.httpclient.AsyncHTTPClient()

        http_client.fetch(self.get_url(), method='POST', body=a,
                          callback=self.on_fetch)

    def get_url(self):
        url_base=options.api_url
        return url_base + self.request.path

    def on_fetch(self, a):
        self.write(str(a.body))
        self.finish()

def save_pid(pid_file, pid):
    with open(pid_file, "w") as f:
        f.write(str(pid))

def main():
    parse_command_line()
    pid = os.fork()
    if options.debug == "" and pid != 0:
        save_pid(options.pid_file, pid)
        exit()

    application = tornado.web.Application([
        (r".*", SwitchOperation),
    ])

    application.listen(int(options.port))
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
