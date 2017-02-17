from google.appengine.ext import db

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
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)
