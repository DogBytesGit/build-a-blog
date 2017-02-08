#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
import webapp2
import jinja2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

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
        self.render("main.html")

#class BlogHandler(webapp2.RequestHanlder):
#    def get(self):
#        #Filters query results to display 5 most recent posts        
#        self.response.write('Displays the 5 most recent posts')

#class NewPostHandler(db.Model):
#    #Invoked to add a new post
#    subject = db.StringProperty(required = True)
#    content = db.TextProperty(required = True)
#    created = db.DateTimeProperty(auto_now_add = True)
#    modified = db.DateTimeProperty(auto_now = True)
#    #author = db.StringProperty(required = True)
#    #rating = db.IntegerProperty(required = False)

#    def render(self):
#        pass


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/blog', BlogHandler),
    ('/newpost', NewPostHandler)
], debug=True)
