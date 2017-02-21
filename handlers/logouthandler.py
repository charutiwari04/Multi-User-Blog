from handlers.bloghandler import *


# Logout Handler
class LogoutPage(BlogHandler):
    def get(self):
        self.logout()
        self.redirect('/blog/login')
