from handlers.bloghandler import *

#### Handler for like for blog post.
class LikeHandler(BlogHandler):
    def get(self, postid):
        if not self.user:
            self.redirect("/blog/login")
    def post(self, postid):
        if not self.user:
            self.redirect("/blog/login")
        else:
            key = db.Key.from_path('BlogsUser', int(postid), parent=blog_key())
            post = db.get(key)
            if self.user.username in post.liked_by:
                #err = "You have already liked this post!"
                #self.render("error.html", error = err)
                newlikes = post.likes - 1
                post.likes = newlikes
                post.liked_by.remove(self.user.username)
                time.sleep(0.1)
                post.put()
                self.redirect("/blog")
            else:
                newlikes = post.likes + 1
                post.likes = newlikes
                post.liked_by.append(self.user.username)
                time.sleep(0.1)
                post.put()
                self.redirect("/blog")
