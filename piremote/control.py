import tornado.websocket
from tornado.log import access_log, app_log
from pykeyboard import PyKeyboard


app_key = ""
k = PyKeyboard()

# a WebSocketHandler object is used to create bidirectional communication
# with the browser
class ControlHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        # returns the value of the argument with the given name from the request
        # query string (the url)
        # it's the key that will be compared with the one saved
        key = self.get_query_argument('key', '')
        if key != app_key:
            access_log.warn('Access denied on %s.' % self.request.remote_ip)
            self.write_message("Access denied")
            self.close()
        else:
            self.write_message("Access granted")
            access_log.info('Access allowed on %s.' % self.request.remote_ip)

    # defines a dictionary
    # deactivate bloc num for keypad_keys and escape_key to work!
    keys = {
        'next': k.page_down_key,
        'prev': k.page_up_key,
        'presentation_mode' : k.function_keys[5], #F5 in Evince
        'open' : k.page_down_key,
        'down' : k.keypad_keys['Down'], 
        'up' : k.keypad_keys['Up'],
        'enter' : k.enter_key,
        'escape' : k.escape_key 
    }
    
    def on_message(self, message):
        try:
            vk = self.keys[message] # the key is next, prev,...
        except KeyError:
            app_log.error('Unknown command: %s' % message)
            return

        # input for the keyboard
        if (message != 'open'):  
            k.tap_key(vk)
        else:
            k.press_keys([k.control_l_key, 'o'])

    def on_close(self):
		access_log.info('Client %s disconnected.' % self.request.remote_ip)
