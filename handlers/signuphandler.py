from handlers.bloghandler import *

#### Handler for Sign up Page
class RegisterPage(BlogHandler):
    def get(self):
        self.render("signup.html")
    def post(self):
        self.username = self.request.get("username")
        self.password = self.request.get("password")
        self.verify = self.request.get("verify")
        self.email = self.request.get("email")
        params = dict(username = self.username,
                      email = self.email)
        PageErr = False

        if  not verify_username(self.username):
            params['error_user'] = "This is not a valid User Name"
            PageErr = True
        
        if not verify_password(self.password):
            params['error_password'] = "This is not a valid Password"
            PageErr = True
        elif self.password != self.verify:
            params['error_password2'] = "Passwords do not match"
            PageErr = True
        
        if not verify_email(self.email):
            params['error_email'] = "That's not a valid Email"
            PageErr = True
        
        if PageErr:
            self.render("signup.html", **params)
        else:
            u = UserForPost.by_name(self.username)
            if u:
                msg = 'That user already exists.'
                self.render("signup.html", error_user = msg)
            else:
                u = UserForPost.register(self.username, self.password, self.email)
                u.put()
                self.login(u)
                self.redirect('/blog/welcome')
