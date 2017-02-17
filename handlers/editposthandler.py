from handlers.bloghandler import *

#### Handler for editing one post
class EditPost(BlogHandler):
    @check_if_valid_post
    def get(self, post_id, post):
        self.render("newpost.html", subject=post.subject, content=post.content)
    @check_if_valid_post
    def post(self, post_id, post):
        subject = self.request.get("subject")
        content = self.request.get("content")
        if subject and content:
            post.subject = subject
            post.content = content
            post.put()
            self.redirect("/blog/%s" % post_id)
        else:
            error = "Both Title and Post are required."
            self.render("newpost.html", subject = subject, content = content, error = error)
