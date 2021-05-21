import time
import webapp2
from google.appengine.api import users, images
from google.appengine.ext import ndb
from webapp2_extras import jinja2
from main import User

# Modelo de la entidad farmacia
class Farmacia(ndb.Model):
    nombre = ndb.StringProperty(required=True)
    direccion = ndb.StringProperty(required=True)
    image_bin = ndb.BlobProperty(required=False)
    userId = ndb.StringProperty(required=True)

# Gestiona la tabla de farmacias
class FarmaciasHandler(webapp2.RequestHandler):

    # Gestiona la vista de todas las farmacias del usuario
    def get(self):

        user = users.get_current_user()

        if user is None:
            self.redirect("/")
        else:
            user_id = user.user_id()
            name_info = user.nickname()
            stored_user = User.query(User.id_user == user_id)

            if stored_user.count() == 0:
                user = User(id_user=user_id, name=name_info)
                user.put()
                time.sleep(1)

            farmacias = Farmacia.query(Farmacia.userId == user_id)
            susts = {
                "user": user,
                "user_logout": users.create_logout_url("/"),
                "farmacias": farmacias
            }

            jinja = jinja2.get_jinja2(app=self.app)
            self.response.write(jinja.render_template("farmacias.html", **susts))

# Gestiona anhadir farmacias
class AnhadirFarmaciasHandler(webapp2.RequestHandler):

    # Gestiona la vista del formulario de anhadir farmacias
    def get(self):

        user = users.get_current_user()

        if user is None:
            self.redirect("/")
        else:
            susts = {
                "user": users.get_current_user(),
                "user_logout": users.create_logout_url("/")
            }

            jinja = jinja2.get_jinja2(app=self.app)
            self.response.write(jinja.render_template("anhadirFarmacias.html", **susts))

    # Gestiona el envio del formulario de anhadir farmacias
    def post(self):

        i = 0
        userId = users.get_current_user().user_id()

        while str(self.request.get("nombre" + str(i + 1))) is not "":
            i += 1
            nombre = self.request.get("nombre" + str(i))
            direccion = self.request.get("direccion" + str(i))
            image_file = self.request.get("img" + str(i), None)
            stored_farmacia = Farmacia.query(ndb.AND(Farmacia.userId == userId, Farmacia.direccion == direccion))

            if stored_farmacia.count() == 0:
                farmacia = Farmacia(nombre=nombre,
                                    direccion=direccion, userId=userId)

                if str(image_file) is not "":
                    farmacia.image_bin = images.resize(image_file, 64, 64)
                else:
                    farmacia.image_bin = None

                farmacia.put()
                time.sleep(1)

        self.redirect("/farmacias")

#Gestiona editar farmacias
class EditarFarmaciasHandler(webapp2.RequestHandler):

    # Gestiona el formulario de editar farmacias
    def get(self):

        farmaciaId = self.request.get("editarFarmaciaActual")

        if farmaciaId is None:
            self.redirect("/farmacias")
        else:
            userId = users.get_current_user().user_id()
            farmacias = Farmacia.query(Farmacia.userId == userId)

            for farmacia in farmacias:
                if str(farmacia.key.id()) == farmaciaId:
                    farmaciaActual = farmacia

            susts = {
                "user": users.get_current_user(),
                "user_logout": users.create_logout_url("/"),
                "farmacia": farmaciaActual
            }

            jinja = jinja2.get_jinja2(app=self.app)
            self.response.write(jinja.render_template("editarFarmacia.html", **susts))

    # Gestiona el envio del formulario de editar farmacias
    def post(self):

        userId = users.get_current_user().user_id()
        farmaciaId = self.request.get("farmaciaActual")
        nombre = self.request.get("nombre")
        direccion = self.request.get("direccion")
        image_file = self.request.get("img", None)
        farmacias = Farmacia.query(Farmacia.userId == userId)

        for farmacia in farmacias:

            if str(farmacia.key.id()) == farmaciaId:
                farmacia.nombre = nombre
                stored_farmacia = Farmacia.query(ndb.AND(Farmacia.userId == userId, Farmacia.direccion == direccion))

                if stored_farmacia.count() == 0:
                    farmacia.direccion = direccion

                if str(image_file) is not "":
                    farmacia.image_bin = images.resize(image_file, 64, 64)

                farmacia.put()
                time.sleep(1)

        self.redirect("/farmacias")

# Gestiona eliminar farmacia
class EliminarFarmaciasHandler(webapp2.RequestHandler):

    # Gestiona la peticion de eliminar farmacia
    def post(self):

        farmaciaId = self.request.get("eliminarFarmaciaActual", None)

        if farmaciaId is not None:

            userId = users.get_current_user().user_id()
            farmacias = Farmacia.query(Farmacia.userId == userId)

            for farmacia in farmacias:
                if str(farmacia.key.id()) == farmaciaId:
                    farmacia.key.delete()
                    time.sleep(1)

        self.redirect("/farmacias")


app = webapp2.WSGIApplication([
    ('/farmacias', FarmaciasHandler),
    ('/anhadirFarmacias', AnhadirFarmaciasHandler),
    ('/editarFarmacias', EditarFarmaciasHandler),
    ('/eliminarFarmacias', EliminarFarmaciasHandler)
], debug=True)
