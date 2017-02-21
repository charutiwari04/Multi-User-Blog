from handlers.bloghandler import *


# Handler for deleting one comment
class DeleteComment(BlogHandler):
    def get(self, postid, userid, commentid):
        if not self.user:
            self.redirect("/blog/login")
        key = db.Key.from_path('BlogsUser', int(postid), parent=blog_key())
        ckey = db.Key.from_path('Comments', int(commentid), parent=key)
        comment = db.get(ckey)
        if not comment:
            self.error(404)
            return
        if self.user.key().id() == comment.user_id:
            db.delete(ckey)
            time.sleep(.1)
            self.redirect("/blog/%s" % postid)
        else:
            err = "You can not delete other User's comment."
            self.render("error.html", error=err)
