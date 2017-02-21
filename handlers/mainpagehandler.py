from handlers.bloghandler import *


# Main page handler redirects to blog page.
class MainPage(BlogHandler):
    def get(self):
        self.redirect("/blog")
