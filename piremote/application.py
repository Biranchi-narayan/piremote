import tornado.web 
import sys
import os
from piremote import control

# retrieve path of static folder
data_dir = os.path.dirname(__file__)
static_path = os.path.join(data_dir, 'static')

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        # open index.html and write the content in the window
        with open(static_path + '/index.html', 'rb') as f:
            self.write(f.read())

# create a tornado web application
application = tornado.web.Application([
    ('/', IndexHandler),
    ('/control', control.ControlHandler),
], static_path=static_path)