from handlers.bloghandler import *

#### Handler for blog page
class BlogPage(BlogHandler):
    def get(self):
        blogs = db.GqlQuery("SELECT * from BlogsUser ORDER BY created DESC LIMIT 10")
        self.render("blog.html", blogs = blogs)
