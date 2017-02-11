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

#Create the database entry
class Art(db.Model):
    title = db.StringProperty(required = True)
    art = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    

class MainPage(Handler):

    def render_front(self, title="", art="", error=""):
        arts = db.GqlQuery("SELECT * FROM Art ORDER BY created DESC ") 
        self.render("front.html", title=title, art=art, error=error, arts=arts)
        
    def get(self):
        #responds to the 'get' when webpage is requested
        self.render_front()

    def post(self):
        #responds when the submit button posts 
        title = self.request.get("title")
        art = self.request.get("art")

        if title and art:
            #create an instance of database entry
            a = Art(title = title, art = art)
            #store the instance in the database
            a.put()
            #when finished redirect to main page
            self.redirect("/")
        else:
            error = "We need both a title and some artwork!"
            self.render_front(title, art, error)

            

app = webapp2.WSGIApplication([
    ('/', MainPage)
], debug=True)
