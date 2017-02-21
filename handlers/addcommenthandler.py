from handlers.bloghandler import *


# Handler for adding one comment to a post.
class AddComment(BlogHandler):
    def get(self, post_id, user_id):
        key = db.Key.from_path('BlogsUser', int(post_id), parent=blog_key())
        post = db.get(key)
        if not self.user:
            if post:
                self.render("/blog/login")
            else:
                self.error(404)
                return
        else:
            self.render("newcomment.html")

    def post(self, post_id, user_id):
        key = db.Key.from_path('BlogsUser', int(post_id), parent=blog_key())
        post = db.get(key)
        if not post:
            self.error(404)
            return
        if not self.user:
            return
        comment = self.request.get("comment")
        if comment:
            c = Comments(parent=key, comment=comment,
                         user_name=self.user.username,
                         post_id=int(post_id), user_id=int(user_id))
            c.put()
            self.redirect('/blog/%s' % post_id)
        else:
            cerror = "Comment is required."
            self.render("newcomment.html", comment=comment, error=cerror)
