from google.appengine.ext import db

#### Definition for Comments datastore which stores all comments and its details.    
class Comments(db.Model):
    comment = db.TextProperty(required = True)
    user_name = db.StringProperty(required = True)
    post_id = db.IntegerProperty(required = True)
    user_id = db.IntegerProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)
