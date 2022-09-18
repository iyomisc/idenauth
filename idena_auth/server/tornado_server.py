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
        self.write('<!DOCTYPE html><html lang="en"><head><title>Idena authentication</title><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><link rel="shortcut icon" href="favicon.ico"/><link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css"><link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Inter"><link rel="icon" href="https://i.imgur.com/CRhZBkd.png"><meta http-equiv="refresh" content="0; URL={}" /><style>body{{font-family:"Inter",Regular;background-color:#4e4e54;}}</style></head><body><div class="container-fluid"><p style="color:#eee;" class="text-center mt-5">Finish the authentication with Idena App<br />If you are not redirected, use this <a href="{}" style="color:#609cff;">link</a></p><img src="https://i.imgur.com/lvZyZCP.png" class="mx-auto d-block mt-5"></div></body></html>'.format(dna_url, dna_url))
        #self.redirect(dna_url)
        
class MainHandler(tornado.web.RequestHandler):
    def get(self, command=""):
        self.write('<!DOCTYPE html><html lang="en"><head><title>Idena authentication</title><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><link rel="shortcut icon" href="favicon.ico"/><link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css"><link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Inter"><link rel="icon" href="https://i.imgur.com/CRhZBkd.png"><style>body{font-family:"Inter",Regular;background-color:#4e4e54;}</style></head><body><div class="container-fluid"><p style="color:#eee;" class="text-center mt-5">You are now logged in!<br>Go back to discord and send <kbd>auth/status</kbd> to the Idena Auth bot in order to get your role</p><img src="https://i.imgur.com/lvZyZCP.png" class="mx-auto d-block mt-5"></div></body></html>')

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [(r"/auth/(.*)", AuthHandler), (r"/(.*)", MainHandler)]
        super(Application, self).__init__(handlers)


def start(port=80):
    app = Application()
    app.listen(port)
    tornado.ioloop.IOLoop.current().start()
