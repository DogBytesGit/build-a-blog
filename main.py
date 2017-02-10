#!/usr/bin/env python

import os
import webapp2
#import jinja

from google.appengine.ext import db

class Handler(webapp2.RequestHandler):
    #This class 
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **parms):
        t = jinja_env.get_template(template)
        return t.render(parms)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class MainPage(Handler):    
    def get(self):
        #This displays the Main Page
        self.render(main.html)

class BlogHandler(webapp2.RequestHanlder):
    def get(self):
        #Filters query results to display 5 most recent posts        
        self.response.write('Displays the 5 most recent posts')

class NewPostHandler(db.Model):
    #Invoked to add a new post
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    modified = db.DateTimeProperty(auto_now = True)
    #author = db.StringProperty(required = True)
    #rating = db.IntegerProperty(required = False)

#    def render(self):
#        pass


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/blog', BlogHandler),
    ('/newpost', NewPostHandler)
], debug=True)
