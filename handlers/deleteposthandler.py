from handlers.bloghandler import *


# Handler for deleting one blog post.
class DeletePost(BlogHandler):
    def get(self, post_id):
        if not self.user:
            self.redirect("/blog/login")
        key = db.Key.from_path('BlogsUser',
                               int(post_id), parent=blog_key())
        post = db.get(key)
        if post:
            if self.user.username != post.username:
                err = "You can not delete other User's Post."
                self.render("error.html", error=err)
            else:
                db.delete(key)
                time.sleep(.1)
                self.redirect("/blog")
        else:
            self.error(404)
            return
