# -*- coding: utf-8 -*-
# @Time : 2022/2/11 15:42
# @Author : su.xinhai
# @Email : su.xinhai@mech-mind.net
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

host = ('0.0.0.0', 50000)


class Resquest(BaseHTTPRequestHandler):

    def do_POST(self):
        data = self.rfile.read(int(self.headers['content-length']))
        get_msg = json.loads(data.decode("utf-8"))
        self.handle_command(get_msg)

    def handle_command(self, data):
        print(data)
        """
        :param get_msg:
        :return:
        """

    def send(self, msg):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(msg).encode('utf-8'))


if __name__ == '__main__':
    server = HTTPServer(host, Resquest)
    print("Starting server, listen at: %s:%s" % host)
    server.serve_forever()
