#!/usr/bin/env python

import os
import webapp2
import jinja2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)


class Handler(webapp2.RequestHandler):
    
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

#Setup the database fields
class BlogPost(db.Model):
    title = db.StringProperty(required = True)
    bPost = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    

class MainPage(Handler):

    def render_main(self, title="", post="", error=""):
        bPosts = db.GqlQuery("SELECT * FROM BlogPost ORDER BY created DESC ") 
        self.render("main.html", bPosts=bPosts)


        
    def get(self):
        #responds to the 'get' when webpage is requested
        self.render_main()

class PostPage(Handler):

    def render_submission(self, title="", bPost="", error=""): 
        self.render("submission.html")
        
    def get(self):
        #responds to the 'get' when webpage is requested
        self.render_submission()
        
    def post(self):
        #responds when the submit button posts 
        title = self.request.get("title")
        bPost = self.request.get("bPost")

        if title and bPost:
            #create an instance of database entry
            p = BlogPost(title = title, bPost = bPost)
            #store the instance in the database
            p.put()
            #when finished redirect to main page
            self.redirect("/")
        else:
            error = "We need both a title and some text!"
            self.render_submission(title, bPost, error)

            

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/post', PostPage)
], debug=True)
