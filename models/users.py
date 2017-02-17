from google.appengine.ext import db
from userauth import *

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
