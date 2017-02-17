from handlers.bloghandler import *

#### Handler for creation of new blog post
class NewblogPage(BlogHandler):
    def get(self):
        if self.user:
            self.render("newpost.html")
        else:
            self.redirect('/blog/loginerr')
    def post(self):
        if self.user:
            subject = self.request.get("subject")
            content = self.request.get("content")
            print "Hello"
            if subject and content:
                b = BlogsUser(parent = blog_key(), subject = subject, username = self.user.username, content = content)
                b.put()
                self.redirect("/blog/%s" % str(b.key().id()))
            else:
                error = "Both Title and Post are required."
                self.render("newpost.html", subject = subject, content = content, error = error)
        else:
            self.redirect('/blog/loginerr')
