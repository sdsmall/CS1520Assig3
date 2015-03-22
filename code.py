import logging
import os
import time
import webapp2
import datetime
import cgi

from google.appengine.api import memcache
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.ext.webapp import template

def render_template(handler, templatename, templatevalues):
  path = os.path.join(os.path.dirname(__file__), 'templates/' + templatename)
  html = template.render(path, templatevalues)
  handler.response.out.write(html)

class Note(ndb.Model):
  name = ndb.StringProperty()
  note_text = ndb.StringProperty()
  user = ndb.StringProperty()
  time = ndb.StringProperty()
  date = ndb.StringProperty()

class EST(datetime.tzinfo):
  def utcoffset(self, dt):
    return datetime.timedelta(hours=-4)

  def dst(self, dt):
    return datetime.timedelta(0)

class MainPage(webapp2.RequestHandler):
  def get(self):
    user = users.get_current_user()
    login = users.create_login_url('/mynotes')
    logout = users.create_logout_url('/')

    template_values = {
      'login': login,
      'logout': logout,
      'user': user
    }
    render_template(self, 'index.html', template_values)

class ErrorPage(webapp2.RequestHandler):
  def get(self):
    code = self.request.get('msg')
    error_msg = 'An unknown error occurred.'

    template_values = {
      'error_msg': error_msg
    }

    render_template(self, 'error.html', template_values)

class UserPage(webapp2.RequestHandler):
  def get(self):
    user = users.get_current_user()

    queryString = '<ul>'

    query = Note.query(Note.user==user.nickname())
    for post in query.iter():
      queryString += "<li>"
      queryString += "<a href=\"/note/"
      queryString += str(post.key.id())
      queryString += "\" "
      queryString += "style=\"text-decoration:none\""
      queryString += ">"
      queryString += post.date
      queryString += ": "
      queryString += post.name
      queryString += "</a>"
      queryString += "</li>"

    queryString += '</ul>'

    template_values = {
      'user': user,
      'queryString': queryString
    }

    render_template(self, 'user.html', template_values)

class EditNote(webapp2.RequestHandler):
  def get(self, note_id):
    user = users.get_current_user()
    post = ndb.Key(Note,int(note_id)).get()
    post_name = post.name
    post_date = post.date
    post_time = post.time
    post_body = post.note_text

    template_values = {
      'user': user,
      'id': note_id,
      'name': post_name,
      'date': post_date,
      'time': post_time,
      'body': post_body
    }

    render_template(self, 'note.html', template_values)

class NewNote(webapp2.RequestHandler):
  def get(self):
    user = users.get_current_user()
    post = Note()
    post.user = user.nickname()
    post.name = "New Note"
    now = datetime.datetime.now(EST())
    post.date = now.strftime("%Y-%m-%d")
    post.time = now.strftime("%I:%M %p")
    post.note_text = ""
    post.put()
    note_id = post.key.id()
    self.redirect('/note/' + str(note_id))

class HandleMessage(webapp2.RequestHandler):
  def post(self):
    user = users.get_current_user()
    if user:
      email = user.email()
      post = Note()

class HandleTitle(webapp2.RequestHandler):
  def post(self):
    title = self.request.get('title')
    note_id = self.request.get('id')
    post = ndb.Key(Note,int(note_id)).get()
    post.name = title
    now = datetime.datetime.now(EST())
    post.date = now.strftime("%Y-%m-%d")
    post.time = now.strftime("%I:%M %p")
    post.put()
    self.response.out.write(post.name + "|" + post.date + "|" + post.time)

class ManualSave(webapp2.RequestHandler):
  def post(self):
    body = self.request.get('body')
    note_id = self.request.get('id')
    post = ndb.Key(Note,int(note_id)).get()
    now = datetime.datetime.now(EST())
    post.date = now.strftime("%Y-%m-%d")
    post.time = now.strftime("%I:%M %p")
    post.note_text = body
    post.put()
    self.response.out.write(post.date + "|" + post.time)

app = webapp2.WSGIApplication([
  ('/', MainPage),
  ('/error', ErrorPage),
  ('/mynotes', UserPage),
  ('/note/(\d+)', EditNote),
  ('/newnote', NewNote),
  ('/savetitle', HandleTitle),
  ('/manualsave', ManualSave)
], debug=True)