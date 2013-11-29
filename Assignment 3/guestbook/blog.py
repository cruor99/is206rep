import os
import re
import random
import hashlib
import hmac
from string import letters
import string
import webapp2
import jinja2
import json
import datetime

from google.appengine.ext import db
#Declare template directory
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)
 #Sets the allowed characters, used in rot13 class
allowed = frozenset(string.ascii_letters + string.digits)
secret = 'fart'
def stringCheck(my_string):
        return all (c in allowed for c in my_string)
        
def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

def make_secure_val(val):
    return '%s|%s' % (val, hmac.new(secret, val).hexdigest())

def check_secure_val(secure_val):
    val = secure_val.split('|')[0]
    if secure_val == make_secure_val(val):
        return val
#Parent class for all blog related classes. 
#Sets up all utility methods for the blog classes.
class BlogHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        params['user'] = self.user
        return render_str(template, **params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def set_secure_cookie(self, name, val):
        cookie_val = make_secure_val(val)
        self.response.headers.add_header(
            'Set-Cookie',
            '%s=%s; Path=/' % (name, cookie_val))

    def read_secure_cookie(self,name):
        cookie_val = self.request.cookies.get(name)
        if cookie_val:
            return check_secure_val(cookie_val)

    def login(self, user):
        self.set_secure_cookie('user_id', str(user.key().id()))

    def logout(self):
        self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')

    def initialize(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)
        uid = self.read_secure_cookie('user_id')
        self.user = uid and User.by_id(int(uid))

def render_post(response, post):
    response.out.write('<b>' + post.subject + '</b><br>')
    response.out.write(post.content)
#Simple collection page, gathering all course-related material
class MainPage(BlogHandler):
  def get(self):
      self.render('samleside.html')


##### user stuff
#Autogenerates salt. Not best form to have it in same file as it's being used.
def make_salt(length = 5):
    return ''.join(random.choice(letters) for x in xrange(length))
#Hashes password based on salt, generates salt if none.
def make_pw_hash(name, pw, salt = None):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s,%s' % (salt, h)
#checks for valid PW
def valid_pw(name, password, h):
    salt = h.split(',')[0]
    return h == make_pw_hash(name, password, salt)

def users_key(group = 'default'):
    return db.Key.from_path('users', group)
#user class
class User(db.Model):
    name = db.StringProperty(required = True)
    pw_hash = db.StringProperty(required = True)
    email = db.StringProperty()

    @classmethod
    def by_id(cls, uid):
        return User.get_by_id(uid, parent = users_key())

    @classmethod
    def by_name(cls, name):
        u = User.all().filter('name =', name).get()
        return u

    @classmethod
    def register(cls, name, pw, email = None):
        pw_hash = make_pw_hash(name, pw)
        return User(parent = users_key(),
                    name = name,
                    pw_hash = pw_hash,
                    email = email)

    @classmethod
    def login(cls, name, pw):
        u = cls.by_name(name)
        if u and valid_pw(name, pw, u.pw_hash):
            return u


##### blog stuff

def blog_key(name = 'default'):
    return db.Key.from_path('blogs', name)
#post database class
class Post(db.Model):
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)

    def render(self):
        self._render_text = self.content.replace('\n', '<br>')
        return render_str("post.html", p = self)
   #json handling for psots
    def toJson(self):
               
        POST_TYPES = (str, str, datetime.date,datetime.date)
        output = {}
        for key in self.properties():
            value = getattr(self, key)
            #date time handler, formats to ISO 8601: YYYY-MM-DD
            if isinstance(value, datetime.date):
                dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime.datetime) else None
                output[key] = json.dumps(value, default=dthandler)
            elif isinstance(value, str):
                output[key] = value
            elif isinstance(value, unicode):
                output[key] = value.decode('unicode-escape')
            elif isinstance(value, db.Model):
                output[key] = to_dict(value)
            else:
                raise ValueError('cannot encode ' + repr(value))
        return output
 #blogfront. Renders all posts by order of created, with the most recent first       
class BlogFront(BlogHandler):
    def get(self):
        posts = greetings = Post.all().order('-created')
        self.render('front.html', posts = posts)
#post page, handles the permalinked posts.
class PostPage(BlogHandler):
    def get(self, post_id):
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(key)

        if not post:
            self.error(404)
            return

        self.render("permalink.html", post = post)
#creation of a new post class
class NewPost(BlogHandler):
    def get(self):
#Checks to make sure you are logged in before posting
        if self.user:
            self.render("newpost.html")
        else:
            self.redirect("/blog/login")
#
    def post(self):
#Another check to make sure you are still logged in before posting the content
        if not self.user:
            self.redirect('/blog')

        subject = self.request.get('subject')
        content = self.request.get('content')
    
        if subject and content:
            p = Post(parent = blog_key(), subject = subject, content = content)
            p.put()
            self.redirect('/blog/%s' % str(p.key().id()))
        else:
            error = "subject and content, please!"
            self.render("newpost.html", subject=subject, content=content, error=error)


#Rot13 class, part of unit 2. Chose to only allow English ascii lettering, returns error if otherwise.
class Rot13(BlogHandler):
    def get(self):
        self.render('rot13-form.html')
 
    def post(self):
        rot13 = ''
        text = self.request.get('text')
#runs strinCheck to make sure text in form is compliant with already establised allowed characters. 
        if stringCheck(text):
            rot13 = text.encode('rot13')
        else:
            rot13 = 'You have input a not-allowed letter. Please limit yourself to the english alphabet'
        self.render('rot13-form.html', text = rot13)


USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)
#Signup klassen
class Signup(BlogHandler):
    def get(self):
        self.render("signup-form.html")

    def post(self):
        have_error = False
        self.username = self.request.get('username')
        self.password = self.request.get('password')
        self.verify = self.request.get('verify')
        self.email = self.request.get('email')

        params = dict(username = self.username,
                      email = self.email)

        if not valid_username(self.username):
            params['error_username'] = "That's not a valid username."
            have_error = True

        if not valid_password(self.password):
            params['error_password'] = "That wasn't a valid password."
            have_error = True
        elif self.password != self.verify:
            params['error_verify'] = "Your passwords didn't match."
            have_error = True

        if not valid_email(self.email):
            params['error_email'] = "That's not a valid email."
            have_error = True

        if have_error:
            self.render('signup-form.html', **params)
        else:
            self.done()

    def done(self, *a, **kw):
        raise NotImplementedError
#Deprecated unit 2 signup
class Unit2Signup(Signup):
    def done(self):
        self.redirect('/unit2/welcome?username=' + self.username)

class Register(Signup):
    def done(self):
        #make sure the user doesn't already exist
        u = User.by_name(self.username)
        if u:
            msg = 'That user already exists.'
            self.render('signup-form.html', error_username = msg)
        else:
            u = User.register(self.username, self.password, self.email)
            u.put()

            self.login(u)
            self.redirect('/blog')
#Login class, would redirect to only /blog but redirects to /blog/welcome for udacity compatability
class Login(BlogHandler):
    def get(self):
        self.render('login-form.html')

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')

        u = User.login(username, password)
        if u:
            self.login(u)
            self.redirect('/blog/welcome')
        else:
            msg = 'Invalid login'
            self.render('login-form.html', error = msg)
#Logout class, would redirect to only /blog but redirects to /blog/signup for udacity compatability
class Logout(BlogHandler):
    def get(self):
        self.logout()
        self.redirect('/blog/signup')

class Welcome(BlogHandler):
    def get(self):
        if self.user:
            self.render('welcome.html', username = self.user.name)
        else:
            self.redirect('/signup')
#Deprecated welcome page for unit 2
class Unit2Welcome(BlogHandler):
    def get(self):
        username = self.request.get('username')
        if valid_username(username):
            self.render('welcome.html', username = username)
        else:
          self.redirect('/unit2/signup')

          
############ JSON stuff
#Seperate json handler for individual post pages, see Post.toJson
class PostPageJson(BlogHandler):
    def get(self, post_id):
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(key)
        if not post:
            self.error(404)
            return
        self.response.headers["Content-Type"] = "application/json; charset=UTF-8"
        self.write(json.dumps(post.toJson()))
#Json dumper for blogfront
class BlogFrontJson(BlogHandler):
    def get(self):
        articles = db.GqlQuery('SELECT * FROM Post '
                               'ORDER BY created DESC '
                               'LIMIT 20')
        content = [{'subject': article.subject,
                    'content': article.content,
                    'created': str(article.created.strftime('%a %b %d %H:%M:%S %Y')),
                    'last_modified': str(article.last_modified.strftime('%a %b %d %H:%M:%S %Y'))
                   } for article in articles]
        self.response.headers['Content-Type'] = 'application/json'
        self.write(json.dumps(content, indent=4))


app = webapp2.WSGIApplication([('/', MainPage),
                               ('/unit2/rot13', Rot13),
                               ('/unit2/signup', Unit2Signup),
                               ('/unit2/welcome', Unit2Welcome),
                               ('/blog/?', BlogFront),
                               ('/blog/([0-9]+)', PostPage),
                               ('/blog/newpost', NewPost),
                               ('/blog/signup', Register),
                               ('/blog/login', Login),
                               ('/logout', Logout),
                               ('/blog/welcome', Welcome),
                               ('/blog.json', BlogFrontJson),
                               ('/blog/.json', BlogFrontJson),#This is here for udacity compatability, their draconic checks only allow for this as the valid link.
                               ('/blog/([0-9]+).json', PostPageJson),
                                ],
                              debug=True)
