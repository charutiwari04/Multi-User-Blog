from handlers.bloghandler import *


# Handler for showing one blog post and its comments
class PostPage(BlogHandler):
    @check_if_valid_post
    def get(self, post_id, post):
        postid = int(post_id)
        comments = db.GqlQuery("SELECT * \
                               from Comments \
                               WHERE post_id=%d \
                               ORDER BY created \
                               DESC" % postid)
        self.render("finalpost.html",
                    post=post,
                    comments=comments)
