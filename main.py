#!/usr/bin/env python

import os
import webapp2
import jinja2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)


class Blog(db.Model):
    title = db.StringProperty(required = True)
    body = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)


class Handler(webapp2.RequestHandler):
    
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))


class Main(Handler):

    def render_main(self, title="", body="", error=""):
        bPosts = db.GqlQuery("SELECT * FROM Blog ORDER BY created DESC LIMIT 5") 
        self.render("main.html", bPosts=bPosts)
        
    def get(self):
        #responds to the 'get' when webpage is requested
        self.render_main()


class NewPost(Handler):

    def render_submission(self, title="", body="", error=""):
        self.render("submission.html", title=title, body=body, error=error)
        
    def get(self):
        #responds to the 'get' when webpage is requested
        self.render_submission()
        
    def post(self):
        #responds when the submit button posts 
        title = self.request.get("title")
        body = self.request.get("body")

        if title and body:
            #create an instance of database entry
            p = Blog(title = title, body = body)
            #store the instance in the database
            p.put()
            #when finished redirect to main page
            self.redirect("/")
        else:
            error = "We need both a title and some text!"
            self.render_submission(title = title, body = body, error = error)


class ViewPost(Handler):

    def get(self, id):
        #responds when a request comes in with a permalink
        id = int(id)
        bPost = Blog.get_by_id(id)
        self.render("post.html", bPost=bPost)            


app = webapp2.WSGIApplication([
    ('/', Main),
	('/blog', Main),
    ('/newpost', NewPost),
    (webapp2.Route('/blog/<id:\d+>', ViewPost))
], debug=True)
