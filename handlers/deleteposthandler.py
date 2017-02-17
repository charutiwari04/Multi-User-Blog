from handlers.bloghandler import *

#### Handler for deleting one blog post.
class DeletePost(BlogHandler):
    def get(self, post_id):
        key = db.Key.from_path('BlogsUser', int(post_id), parent=blog_key())
        post = db.get(key)
        if post:
            db.delete(key)
            time.sleep(.1)
            self.redirect("/blog")
        else:
            self.error(404)
            return
