import tornado.ioloop
import tornado.web

from idena_auth.auth import auth



class AuthHandler(tornado.web.RequestHandler):
    def nonce(self):
        request = self.request.body.decode("utf-8")
        print(request)
        self.write(auth.get_nonce_response(request, as_json=False))

    def authentication(self):
        request = self.request.body.decode("utf-8")
        print(request)
        self.write(auth.get_authentication_response(request, as_json=False))

    def post(self, command):
        print(command, self.request.uri)
        if command:
            getattr(self, command.split("/")[0])()
    
    def get(self, command=""):
        if not command:
            return
            
        if not auth.db.is_token_registered(command):
            return
        
        if auth.db.is_token_auth(command):
            return
        dna_url = auth.get_dna_url(token=command)
        self.write('<head><meta http-equiv="refresh" content="0; URL={}" /></head>If you are not redirected, use this <a href="{}">link</a>'.format(dna_url, dna_url))
        #self.redirect(dna_url)
        
class MainHandler(tornado.web.RequestHandler):
    def get(self, command=""):
        self.write("You are now logged!<br>Go back to discord and send <input value='auth/status'> to The Idenauth bot in order to get your role")

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [(r"/auth/(.*)", AuthHandler), (r"/(.*)", MainHandler)]
        super(Application, self).__init__(handlers)


def start(port=8888):
    app = Application()
    app.listen(port)
    tornado.ioloop.IOLoop.current().start()
