from handlers.bloghandler import *


# Handler for editing one comment
class EditComment(BlogHandler):
    def get(self, postid, userid, commentid):
        if not self.user:
            self.redirect("/blog/login")
        key = db.Key.from_path('BlogsUser',
                               int(postid), parent=blog_key())
        ckey = db.Key.from_path('Comments',
                                int(commentid), parent=key)
        comment = db.get(ckey)
        if comment:
            if self.user.key().id() == comment.user_id:
                self.render("newcomment.html",
                            comment=comment.comment)
            else:
                err = "You can not edit other User's comment."
                self.render("error.html", error=err)
        else:
            self.error(404)
            return

    def post(self, postid, userid, commentid):
        if not self.user:
            return
        commentInp = self.request.get("comment")
        key = db.Key.from_path('BlogsUser',
                               int(postid), parent=blog_key())
        ckey = db.Key.from_path('Comments',
                                int(commentid), parent=key)
        comment = db.get(ckey)
        if not comment:
            self.error(404)
            return
        if self.user.key().id() == comment.user_id:
            if commentInp:
                comment.comment = commentInp
                comment.put()
                time.sleep(.1)
                self.redirect("/blog/%s" % postid)
            else:
                cerror = "Comment is required."
                self.render("newcomment.html", error=cerror)
        else:
            err = "You can not edit other User's comment."
            self.render("error.html", error=err)
