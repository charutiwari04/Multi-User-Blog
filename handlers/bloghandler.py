import os
import webapp2
import jinja2
import time
from functools import wraps
from models.blogs import *
from models.users import *
from models.comments import *
from userauth import *

# Code for rendering the templates on webpage using jinja2.
template_dir = os.path.join(os.path.dirname(__file__), '../templates')
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
        self.message = 'Can not post on blog, You need to login.'
def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

#### check_if_valid_post decorator
def check_if_valid_post(function):
    @wraps(function)
    def wrapper(self, post_id):
        key = db.Key.from_path('BlogsUser', int(post_id), parent=blog_key())
        post = db.get(key)
        if post:
            return function(self, post_id, post)
        else:
            self.error(404)
            return
    return wrapper

