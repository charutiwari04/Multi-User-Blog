import os
import re
import time
import random
import hashlib
import hmac
from string import letters
import webapp2
import jinja2
from google.appengine.ext import db

# Code for rendering the templates on webpage using jinja2.
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)
class BlogHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.write(*a, **kw)

    def render_str(self, template, **params):
        params['user'] = self.user
        return render_str(template, **params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))
        
    # making cookie secured value
    def set_secure_cookie(self, name, val):
        cookie_val = make_hash(val)
        self.response.headers.add_header('Set-Cookie', '%s=%s; Path=/' % (name, cookie_val))
        
    # find the received cookie value
    def check_secure_cookie(self, name):
        cook_val = self.request.cookies.get(name)
        return (cook_val and check_hash_value(cook_val))

    # set cookie
    def login(self, user):
        self.set_secure_cookie('user_id', str(user.key().id()))
        
    # delete all cookies    
    def logout(self):
        self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')

    # Initialize the user id if user is login.
    def initialize(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)
        uid = self.check_secure_cookie('user_id')
        self.user = uid and UserForPost.by_id(int(uid))
        self.message = 'Can not post on blog, User need to login.'
        
def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

def render_post(response, post):
    response.out.write('<b>' + post.subject + '</b><br>')
    response.out.write(post.content)

#### Main page handler redirects to blog page.
class MainPage(BlogHandler):
    def get(self):
        self.redirect("/blog")
        
#### get the key for blog
def blog_key(name = 'default'):
    return db.Key.from_path('blogs', name)

#### Definition for Blogs datastore which stores all blogs and its details.
class BlogsUser(db.Model):
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    username = db.StringProperty(required = True)
    likes = db.IntegerProperty(default = 0)
    liked_by = db.StringListProperty()
    unlikes = db.IntegerProperty(default = 0)
    unliked_by = db.StringListProperty()
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)

#### Definition for Comments datastore which stores all comments and its details.    
class Comments(db.Model):
    comment = db.TextProperty(required = True)
    user_name = db.StringProperty(required = True)
    post_id = db.IntegerProperty(required = True)
    user_id = db.IntegerProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)

#### Handler for blog page
class BlogPage(BlogHandler):
    def get(self):
        blogs = db.GqlQuery("SELECT * from BlogsUser ORDER BY created DESC LIMIT 10")
        self.render("blog.html", blogs = blogs)

#### Handler for creation of new blog post
class NewblogPage(BlogHandler):
    def get(self):
        if self.user:
            self.render("newpost.html")
        else:
            self.redirect('/blog/loginerr')
    def post(self):
        if self.user:
            subject = self.request.get("subject")
            content = self.request.get("content")
            print "Hello"
            if subject and content:
                b = BlogsUser(parent = blog_key(), subject = subject, username = self.user.username, content = content)
                b.put()
                self.redirect("/blog/%s" % str(b.key().id()))
            else:
                error = "Both Title and Post are required."
                self.render("newpost.html", subject = subject, content = content, error = error)
        else:
            self.redirect('/blog/loginerr')

#### Handler for showing one blog post and its comments
class PostPage(BlogHandler):
    def get(self, post_id):
        key = db.Key.from_path('BlogsUser', int(post_id), parent=blog_key())
        post = db.get(key)
        postid = int(post_id)
        if not post:
            self.error(404)
            return
        comments = db.GqlQuery("SELECT * from Comments WHERE post_id=%d ORDER BY created DESC" %postid)
        self.render("finalpost.html", post = post, comments = comments)

#### Handler for editing one post
class EditPost(BlogHandler):
    def get(self, post_id=""):
        if post_id:
            key = db.Key.from_path('BlogsUser', int(post_id), parent=blog_key())
            post = db.get(key)
            self.render("newpost.html", subject=post.subject, content=post.content)
    def post(self, post_id=""):
        subject = self.request.get("subject")
        content = self.request.get("content")
        if subject and content:
            key = db.Key.from_path('BlogsUser', int(post_id), parent=blog_key())
            post = db.get(key)
            post.subject = subject
            post.content = content
            post.put()
            self.redirect("/blog/%s" % post_id)
        else:
            error = "Both Title and Post are required."
            self.render("newpost.html", subject = subject, content = content, error = error)

#### Handler for deleting one blog post.
class DeletePost(BlogHandler):
    def get(self, post_id):
        if post_id:
            key = db.Key.from_path('BlogsUser', int(post_id), parent=blog_key())
            db.delete(key)
            time.sleep(.1)
            self.redirect("/blog")

#### Handler for adding one comment to a post.
class AddComment(BlogHandler):
    def get(self, post_id, user_id):
        if not self.user:
            self.render("/blog/login")
        else:
            self.render("newcomment.html")
    def post(self, post_id, user_id):
        if not self.user:
            return
        comment = self.request.get("comment")
        if comment:
            key = db.Key.from_path('BlogsUser', int(post_id), parent=blog_key())
            c = Comments(parent=key, comment=comment, user_name = self.user.username, post_id=int(post_id), user_id=int(user_id))
            c.put()
            self.redirect('/blog/%s' % post_id)
        else:
            cerror = "Comment is required."
            self.render("newcomment.html", comment = comment, error = cerror)

#### Handler for editing one comment
class EditComment(BlogHandler):
    def get(self, postid, userid, commentid):
        if not self.user:
            self.redirect("/blog/login")
        key = db.Key.from_path('BlogsUser', int(postid), parent=blog_key())
        ckey = db.Key.from_path('Comments', int(commentid), parent=key)
        comment = db.get(ckey)
        if self.user.key().id() == comment.user_id:
            self.render("newcomment.html", comment = comment.comment)
        else:
            err = "You can not edit other User's comment."
            self.render("error.html", error = err)
    def post(self, postid, userid, commentid):
        if not self.user:
            return
        commentInp = self.request.get("comment")
        key = db.Key.from_path('BlogsUser', int(postid), parent=blog_key())
        ckey = db.Key.from_path('Comments', int(commentid), parent=key)
        comment = db.get(ckey)
        if self.user.key().id() == comment.user_id:
            if commentInp:
                comment.comment = commentInp
                comment.put()
                time.sleep(.1)
                self.redirect("/blog/%s" % postid)
            else:
                cerror = "Comment is required."
                self.render("newcomment.html", error = cerror)
        else:
            err = "You can not edit other User's comment."
            self.render("error.html", error = err)

#### Handler for deleting one comment
class DeleteComment(BlogHandler):
    def get(self, postid, userid, commentid):
        if not self.user:
            self.redirect("/blog/login")
        key = db.Key.from_path('BlogsUser', int(postid), parent=blog_key())
        ckey = db.Key.from_path('Comments', int(commentid), parent=key)
        comment = db.get(ckey)
        if self.user.key().id() == comment.user_id:
            db.delete(ckey)
            time.sleep(.1)
            self.redirect("/blog/%s" % postid)
        else:
            err = "You can not delete other User's comment."
            self.render("error.html", error = err)

#### Handler for like for blog post.
class LikeHandler(BlogHandler):
    def get(self, postid):
        if not self.user:
            self.redirect("/blog/login")
    def post(self, postid):
        if not self.user:
            self.redirect("/blog/login")
        else:
            key = db.Key.from_path('BlogsUser', int(postid), parent=blog_key())
            post = db.get(key)
            if self.user.username in post.liked_by:
                err = "You have already liked this post!"
                self.render("error.html", error = err)
            else:
                newlikes = post.likes + 1
                post.likes = newlikes
                post.liked_by.append(self.user.username)
                post.put()
                self.redirect("/blog")

#### Handler for unlike for blog post.
class UnlikeHandler(BlogHandler):
    def get(self, postid):
        if not self.user:
            self.redirect("/blog/login")
    def post(self, postid):
        if not self.user:
            self.redirect("/blog/login")
        else:
            key = db.Key.from_path('BlogsUser', int(postid), parent=blog_key())
            post = db.get(key)
            if self.user.username in post.unliked_by:
                err = "You have already unliked this post!"
                self.render("error.html", error = err)
            else:
                newlikes = post.unlikes + 1
                post.unlikes = newlikes
                post.unliked_by.append(self.user.username)
                post.put()
                self.redirect("/blog")
                
#### Form Validation functions 
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def verify_username(username):
    return username and USER_RE.match(username)
PASS_RE = re.compile(r"^.{3,20}$")
def verify_password(password):
    return password and PASS_RE.match(password)
EMAIL_RE = re.compile(r'^[\S]+@[\S]+.[\S]+$')
def verify_email(email):
    return not email or EMAIL_RE.match(email)

#### Database setup and functions
def user_key(name = 'default'):
    return db.Key.from_path('users', name)
class UserForPost(db.Model):
    username = db.StringProperty(required = True)
    pwd_hash = db.StringProperty(required = True)
    email = db.StringProperty()
    @classmethod
    def by_id(cls, uid):
        return UserForPost.get_by_id(uid, parent = user_key())

    @classmethod
    def by_name(cls, name):
        u = UserForPost.all().filter('username =', name).get()
        return u
    
    @classmethod
    def register(cls, name, pw, email = None):
        pw_hash = make_pw_hash(name, pw)
        return UserForPost(parent = user_key(),
                    username = name,
                    pwd_hash = pw_hash,
                    email = email)
    @classmethod
    def login(cls, name, pw):
        u = cls.by_name(name)
        if u and check_valid_pw(name, pw, u.pwd_hash):
            return u

#### Handling the hashing of password and checking valid password functions
SECRET = 'hjhdfuasoi*&^%$$$JHGFghjsdnjxsjd'
def send_random_string(length = 5):
    rndm = ''.join([random.choice(letters) for n in xrange(length)])
    return rndm
def make_hash(val):
    return '%s|%s' % (val, hmac.new(SECRET, val).hexdigest())
def check_hash_value(h):
    hNew = h.split('|')[0]
    if h == make_hash(hNew):
        return hNew
def make_pw_hash(name, pwd, salt = None):
    if not salt:
        salt = send_random_string()
    h = hashlib.sha256(name + pwd + salt).hexdigest()
    return '%s,%s' % (salt, h)
def check_valid_pw(name, password, hash_paswd):
    salt = hash_paswd.split(',')[0]
    return hash_paswd == make_pw_hash(name, password, salt)

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

#### Login Handler
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
            self.render("login.html", error = msg)

#### Logout Handler
class LogoutPage(BlogHandler):
    def get(self):
        self.logout()
        #self.redirect('/blog/registration')
        self.redirect('/blog/login')

#### Welcome Handler
class WelcomePage(BlogHandler):
    def get(self):
        if  self.user:
            self.render("welcome.html", username = self.user.username)
        else:
            self.redirect('/blog/registration')
#### Error Handler
class LoginError(BlogHandler):
    def get(self):
        self.render("login-error.html", message = self.message)
        
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/blog', BlogPage),
    ('/blog/newpost', NewblogPage),
    ('/blog/([0-9]+)', PostPage),
    ('/blog/registration', RegisterPage),
    ('/blog/login', LoginPage),
    ('/blog/logout', LogoutPage),
    ('/blog/welcome', WelcomePage),
    ('/blog/edit/([0-9]+)', EditPost),
    ('/blog/loginerr/?', LoginError),
    ('/blog/delete/([0-9]+)', DeletePost),
    ('/blog/([0-9]+)/addcomment/([0-9]+)', AddComment),
    ('/blog/([0-9]+)/([0-9]+)/editcomment/([0-9]+)', EditComment),
    ('/blog/([0-9]+)/([0-9]+)/deletecomment/([0-9]+)', DeleteComment),
    ('/blog/like/([0-9]+)', LikeHandler),
    ('/blog/unlike/([0-9]+)', UnlikeHandler),
    ], debug=True)

