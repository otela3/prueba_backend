from sqlalchemy.orm import Session
from starlette import responses
from starlette.responses import Response
from model.request import registerRequest
from model.response import dataUsuario, defaultResponse, responseAutenticacion
from database.models import UsuarioTabla
from database import database
from database import models


def _add_tables():
    return database.Base.metadata.create_all(bind=database.engine)


def validarUsuario(email: str, password: str, db: Session) -> responseAutenticacion:
    usuario: UsuarioTabla = db.query(UsuarioTabla).filter(UsuarioTabla.email == email). \
        filter(UsuarioTabla.password == password).first()
    if usuario is None:
        response = responseAutenticacion(resultado="error", mensaje="Usuario no valido")
        return response
    response: responseAutenticacion = responseAutenticacion()
    response.usuario = dataUsuario.from_orm(usuario)
    return response


def registrar(request: registerRequest, db: Session) -> defaultResponse:
    response: defaultResponse = defaultResponse()
    newUser: UsuarioTabla = UsuarioTabla()
    email = db.query(UsuarioTabla).filter(UsuarioTabla.email == request.email).first()
    if email is None:
        newUser.idusuario = None
        newUser.email = request.email
        newUser.password = request.password
        newUser.es_admin = request.es_admin

        db.add(newUser)
        db.commit()

        response.resultado = "ok"
        response.mensaje = "usuario registrado correctamente"
        return response
    else:
        response.resultado = "error"
        response.mensaje = "este correo ya existe"
        return response

def registrarGoogle(email: str, db: Session):
    newUsuario: UsuarioTabla = UsuarioTabla()
    newUsuario.idusuario = None
    newUsuario.email = email
    newUsuario.password = "123"
    newUsuario.es_admin = False
    db.add(newUsuario)
    db.commit()
    return "ok"

def validarUsuarioGoogle(email: str, password: str, db: Session) -> responseAutenticacion:
    usuario: UsuarioTabla = db.query(UsuarioTabla).filter(UsuarioTabla.email == email).filter(UsuarioTabla.password == password).first()
    if usuario is None:
        response = responseAutenticacion(resultado="error", mensaje="Usuario no válido")
        return response
    response: responseAutenticacion = responseAutenticacion()
    response.usuario = dataUsuario.from_orm(usuario)
    return response