from handlers.signuphandler import *
from handlers.loginhandler import *
from handlers.logouthandler import *
from handlers.mainpagehandler import *
from handlers.blogpagehandler import *
from handlers.newblogpage import *
from handlers.postpagehandler import *
from handlers.editposthandler import *
from handlers.deleteposthandler import *
from handlers.addcommenthandler import *
from handlers.editcommenthandler import *
from handlers.deletecommenthandler import *
from handlers.likehandler import *
from handlers.welcomehandler import *
from handlers.errorhandler import *

def render_post(response, post):
    response.out.write('<b>' + post.subject + '</b><br>')
    response.out.write(post.content)

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/blog', BlogPage),
    ('/blog/newpost', NewblogPage),
    ('/blog/([0-9]+)', PostPage),
    ('/blog/registration', RegisterPage),
    ('/blog/login', LoginPage),
    ('/blog/logout', LogoutPage),
    ('/blog/welcome', WelcomePage),
    ('/blog/edit/([0-9]+)', EditPost),
    ('/blog/loginerr/?', LoginError),
    ('/blog/delete/([0-9]+)', DeletePost),
    ('/blog/([0-9]+)/addcomment/([0-9]+)', AddComment),
    ('/blog/([0-9]+)/([0-9]+)/editcomment/([0-9]+)', EditComment),
    ('/blog/([0-9]+)/([0-9]+)/deletecomment/([0-9]+)', DeleteComment),
    ('/blog/like/([0-9]+)', LikeHandler),
    ], debug=True)

