from handlers.bloghandler import *

#### Welcome Handler
class WelcomePage(BlogHandler):
    def get(self):
        if  self.user:
            self.render("welcome.html", username = self.user.username)
        else:
            self.redirect('/blog/registration')

