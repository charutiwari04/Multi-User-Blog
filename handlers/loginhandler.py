from handlers.bloghandler import *


# Login Handler
class LoginPage(BlogHandler):
    def get(self):
        self.render("login.html")

    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")
        u = UserForPost.login(username, password)
        if u:
            self.login(u)
            self.redirect('/')
        else:
            msg = "Invalid User"
            self.render("login.html", error=msg)
