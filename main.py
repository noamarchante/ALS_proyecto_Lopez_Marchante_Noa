import webapp2
from google.appengine.ext import ndb
from google.appengine.api import users


# Modelo de la entidad usuarios
class User(ndb.Model):
    id_user = ndb.StringProperty(required=True)
    name = ndb.StringProperty(required=True)


# Gestiona el comportamiento inicial de la aplicacion
class MainHandler(webapp2.RequestHandler):

    def get(self):

        user = users.get_current_user()

        if user:
            self.redirect("/farmacias")
        else:
            self.redirect(users.create_login_url("/"))


app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
