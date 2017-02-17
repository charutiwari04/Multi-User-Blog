import re
import random
import hashlib
import hmac
from string import letters
from google.appengine.ext import db

#### Form Validation functions 
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def verify_username(username):
    return username and USER_RE.match(username)
PASS_RE = re.compile(r"^.{3,20}$")
def verify_password(password):
    return password and PASS_RE.match(password)
EMAIL_RE = re.compile(r'^[\S]+@[\S]+.[\S]+$')
def verify_email(email):
    return not email or EMAIL_RE.match(email)


#### Handling the hashing of password and checking valid password functions
SECRET = 'hjhdfuasoi*&^%$$$JHGFghjsdnjxsjd'
def send_random_string(length = 5):
    rndm = ''.join([random.choice(letters) for n in xrange(length)])
    return rndm
def make_hash(val):
    return '%s|%s' % (val, hmac.new(SECRET, val).hexdigest())
def check_hash_value(h):
    hNew = h.split('|')[0]
    if h == make_hash(hNew):
        return hNew
def make_pw_hash(name, pwd, salt = None):
    if not salt:
        salt = send_random_string()
    h = hashlib.sha256(name + pwd + salt).hexdigest()
    return '%s,%s' % (salt, h)
def check_valid_pw(name, password, hash_paswd):
    salt = hash_paswd.split(',')[0]
    return hash_paswd == make_pw_hash(name, password, salt)
