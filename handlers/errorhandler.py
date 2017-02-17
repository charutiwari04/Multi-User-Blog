from handlers.bloghandler import *

#### Error Handler
class LoginError(BlogHandler):
    def get(self):
        self.render("login-error.html", message = self.message)
