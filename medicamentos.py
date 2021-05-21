# coding=utf-8
import time
from datetime import datetime
import webapp2
from google.appengine.api import users, images
from google.appengine.ext import ndb
from webapp2_extras import jinja2
from farmacias import Farmacia

# Modelo de la entidad medicamento
class Medicamento(ndb.Model):
    nombre = ndb.StringProperty(required=True)
    descripcion = ndb.StringProperty(required=True)
    laboratorio = ndb.StringProperty(required=True)
    proveedor = ndb.StringProperty(required=True)
    cantidad = ndb.IntegerProperty(required=True)
    fechaCaducidad = ndb.DateProperty(required=True)
    tipoMedicamento = ndb.StringProperty(required=True)
    image_bin = ndb.BlobProperty(required=False)
    farmaciaId = ndb.StringProperty(required=True)


# Gestiona los medicamentos de una farmacia
class MedicamentosHandler(webapp2.RequestHandler):

    # Gestiona la vista de la tabla de medicamentos de una farmacia
    def get(self):

        farmaciaId = self.request.get("medicamentoFarmaciaActual", None)

        if farmaciaId is None:
            self.redirect("/farmacias")
        else:
            farmacias = Farmacia.query(Farmacia.userId == str(users.get_current_user().user_id()))

            for farmacia in farmacias:
                if str(farmacia.key.id()) == farmaciaId:
                    farmaciaActual = farmacia

            medicamentos = Medicamento.query(Medicamento.farmaciaId == farmaciaId)

            susts = {
                "user": users.get_current_user(),
                "user_logout": users.create_logout_url("/"),
                "farmacia": farmaciaActual,
                "medicamentos": medicamentos
            }

            jinja = jinja2.get_jinja2(app=self.app)
            self.response.write(jinja.render_template("medicamentos.html", **susts))


# Gestiona anhadir medicamentos
class AnhadirMedicamentosHandler(webapp2.RequestHandler):

    # Gestiona la vista de anhadir medicamentos
    def get(self):

        farmaciaId = self.request.get("anhadirMedicamentosFarmaciaActual")

        if farmaciaId is None:
            self.redirect("/farmacias")
        else:
            farmacias = Farmacia.query(Farmacia.userId == str(users.get_current_user().user_id()))

            for farmacia in farmacias:
                if str(farmacia.key.id()) == farmaciaId:
                    farmaciaActual = farmacia

            tiposMedicamentos = [
                "ANALGESICO",
                "ANTIACIDO",
                "ANTIULCEROSO",
                "ANTIALERGICO",
                "ANTIDIARREICO",
                "LAXANTE",
                "ANTIINFLAMATORIO",
                "ANTIINFECCIOSO",
                "ANTIPIRETICO",
                "ANTITUSIVO",
                "MUCOLITICO"
            ]

            susts = {
                "user": users.get_current_user(),
                "user_logout": users.create_logout_url("/"),
                "farmacia": farmaciaActual,
                "tiposMedicamentos": tiposMedicamentos
            }

            jinja = jinja2.get_jinja2(app=self.app)
            self.response.write(jinja.render_template("anhadirMedicamentos.html", **susts))

    # Gestiona el envio del formulario de anhadir medicamentos
    def post(self):

        i = 0
        farmaciaId = self.request.get("medicamentoFarmaciaActual", None)
        farmacias = Farmacia.query(Farmacia.userId == str(users.get_current_user().user_id()))
        volver = self.request.get("volver", None)
        farmaciaIdVolver = self.request.get("medicamentoFarmaciaActualVolver", None)

        if farmaciaId is None:
            farmaciaId = farmaciaIdVolver

        for farmacia in farmacias:
            if str(farmacia.key.id()) == farmaciaId:
                farmaciaActual = farmacia

        if volver is None:
            while str(self.request.get("nombre" + str(i + 1))) is not "":
                i += 1
                nombre = self.request.get("nombre" + str(i))
                descripcion = self.request.get("descripcion" + str(i))
                laboratorio = self.request.get("laboratorio" + str(i))
                proveedor = self.request.get("proveedor" + str(i))
                cantidad = int(self.request.get("cantidad" + str(i)))
                fechaCaducidad = datetime.strptime(self.request.get("fechaCaducidad" + str(i)), '%Y-%m-%d')
                tipoMedicamento = self.request.get("tipoMedicamento" + str(i))
                image_file = self.request.get("img" + str(i), None)
                stored_medicamento = Medicamento.query(
                    ndb.AND(Medicamento.farmaciaId == farmaciaId, Medicamento.nombre == nombre))

                if stored_medicamento.count() == 0:
                    medicamento = Medicamento(nombre=nombre,
                                              descripcion=descripcion, laboratorio=laboratorio, proveedor=proveedor,
                                              cantidad=cantidad, fechaCaducidad=fechaCaducidad,
                                              tipoMedicamento=tipoMedicamento, farmaciaId=farmaciaId)

                    if str(image_file) is not "":
                        medicamento.image_bin = images.resize(image_file, 64, 64)
                    else:
                        medicamento.image_bin = None

                    medicamento.put()
                    time.sleep(1)

        medicamentos = Medicamento.query(Medicamento.farmaciaId == farmaciaId)

        susts = {
            "user": users.get_current_user(),
            "farmacia": farmaciaActual,
            "medicamentos": medicamentos
        }

        jinja = jinja2.get_jinja2(app=self.app)
        self.response.write(jinja.render_template("medicamentos.html", **susts))

# Gestiona editar medicamentos
class EditarMedicamentosHandler(webapp2.RequestHandler):

    # Gestiona la vista de editar medicamentos
    def get(self):

        farmaciaId = self.request.get("editarMedicamentosFarmaciaActual")
        nombreActual = self.request.get("nombreMedicamentoActual")

        if farmaciaId is None:
            self.redirect("/farmacias")
        else:
            farmacias = Farmacia.query(Farmacia.userId == str(users.get_current_user().user_id()))

            for farmacia in farmacias:
                if str(farmacia.key.id()) == farmaciaId:
                    farmaciaActual = farmacia

            tiposMedicamentos = [
                "ANALGESICO",
                "ANTIACIDO",
                "ANTIULCEROSO",
                "ANTIALERGICO",
                "ANTIDIARREICO",
                "LAXANTE",
                "ANTIINFLAMATORIO",
                "ANTIINFECCIOSO",
                "ANTIPIRETICO",
                "ANTITUSIVO",
                "MUCOLITICO"
            ]

            medicamento = Medicamento.query(
                ndb.AND(Medicamento.farmaciaId == farmaciaId, Medicamento.nombre == nombreActual)).get()

            tiposMedicamentos.remove(medicamento.tipoMedicamento)

            susts = {
                "user": users.get_current_user(),
                "user_logout": users.create_logout_url("/"),
                "medicamento": medicamento,
                "tiposMedicamentos": tiposMedicamentos,
                "farmacia": farmaciaActual
            }

            jinja = jinja2.get_jinja2(app=self.app)
            self.response.write(jinja.render_template("editarMedicamento.html", **susts))

    # Gestiona el envio del formulario de editar medicamentos
    def post(self):
        volver = self.request.get("volver", None)
        nombreActual = self.request.get("nombreMedicamentoActual")
        farmaciaId = self.request.get("medicamentoFarmaciaActual")
        farmacias = Farmacia.query(Farmacia.userId == str(users.get_current_user().user_id()))

        for farmacia in farmacias:

            if str(farmacia.key.id()) == farmaciaId:

                farmaciaActual = farmacia

        if volver is None:

            nombre = self.request.get("nombre")
            descripcion = self.request.get("descripcion")
            laboratorio = self.request.get("laboratorio")
            proveedor = self.request.get("proveedor")
            cantidad = int(self.request.get("cantidad"))
            fechaCaducidad = datetime.strptime(self.request.get("fechaCaducidad"), '%Y-%m-%d')
            tipoMedicamento = self.request.get("tipoMedicamento")
            image_file = self.request.get("img", None)

            medicamentos = Medicamento.query(Medicamento.farmaciaId == farmaciaId)

            for medicamento in medicamentos:

                if str(medicamento.nombre) == nombreActual:

                    stored_medicamento = Medicamento.query(
                        ndb.AND(Medicamento.farmaciaId == farmaciaId, Medicamento.nombre == nombre))

                    if stored_medicamento.count() == 0:
                        medicamento.nombre = nombre

                    medicamento.descripcion = descripcion
                    medicamento.laboratorio = laboratorio
                    medicamento.proveedor = proveedor
                    medicamento.cantidad = cantidad
                    medicamento.fechaCaducidad = fechaCaducidad
                    medicamento.tipoMedicamento = tipoMedicamento

                    if str(image_file) is not "":
                        medicamento.image_bin = images.resize(image_file, 64, 64)

                    medicamento.put()
                    time.sleep(1)

        medicamentos = Medicamento.query(Medicamento.farmaciaId == farmaciaId)

        susts = {
            "user": users.get_current_user(),
            "farmacia": farmaciaActual,
            "medicamentos": medicamentos
        }

        jinja = jinja2.get_jinja2(app=self.app)
        self.response.write(jinja.render_template("medicamentos.html", **susts))


# Gestiona eliminar medicamentos
class EliminarMedicamentosHandler(webapp2.RequestHandler):

    # Gestiona la peticion de eliminar medicamentos
    def post(self):

        farmaciaId = self.request.get("eliminarMedicamentosFarmaciaActual", None)
        nombreMedicamento = self.request.get("nombreMedicamento", None)

        if farmaciaId is not None:
            medicamentos = Medicamento.query(Medicamento.farmaciaId == farmaciaId)
            for medicamento in medicamentos:
                if str(medicamento.nombre) == nombreMedicamento:
                    medicamento.key.delete()
                    time.sleep(1)

        farmacias = Farmacia.query(Farmacia.userId == str(users.get_current_user().user_id()))

        for farmacia in farmacias:
            if str(farmacia.key.id()) == farmaciaId:
                farmaciaActual = farmacia

        medicamentos = Medicamento.query(Medicamento.farmaciaId == farmaciaId)

        susts = {
            "farmacia": farmaciaActual,
            "medicamentos": medicamentos
        }

        jinja = jinja2.get_jinja2(app=self.app)
        self.response.write(jinja.render_template("medicamentos.html", **susts))


app = webapp2.WSGIApplication([
    ('/medicamentos', MedicamentosHandler),
    ('/anhadirMedicamentos', AnhadirMedicamentosHandler),
    ('/editarMedicamentos', EditarMedicamentosHandler),
    ('/eliminarMedicamentos', EliminarMedicamentosHandler)
], debug=True)
