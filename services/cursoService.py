from typing import List
from sqlalchemy.orm import Session
from starlette import responses
from model.request import crearCursoRequest, suscribirCursoRequest
from model.response import defaultResponse, cursosResponse, curso
from database.models import CursoTabla, SubTabla

def curso_crear(request: crearCursoRequest, db: Session, session) -> defaultResponse:
    response: defaultResponse = defaultResponse()
    curso: CursoTabla = CursoTabla()
    if session["es_admin"] is True:
        curso.idcurso = None
        curso.titulo = request.titulo
        curso.descripcion = request.descripcion
        db.add(curso)
        db.commit()
        response.resultado = "ok"
        response.mensaje = "curso creado correctamente"
        return response
    else:
        response.resultado = "error"
        return response

def curso_listar(db: Session) -> cursosResponse:
    response: cursosResponse = cursosResponse()
    cursos: List[curso] = []
    curso_tabla = db.query(CursoTabla).all()
    for cur in curso_tabla:
        i: curso = curso()
        i.idcurso = cur.idcurso
        i.titulo = cur.titulo
        i.descripcion = cur.descripcion
        cursos.append(i)
    response.cursos = cursos
    response.resultado = "ok"
    return response

def curso_eliminar(id_curso, session, db: Session) -> defaultResponse:
    response: defaultResponse = defaultResponse()
    if session["es_admin"] is True:
        curso_tabla = db.query(CursoTabla).filter(CursoTabla.idcurso == id_curso).first()
        db.delete(curso_tabla)
        db.commit()
        response.resultado = "ok"
        response.mensaje = "curso eliminado correctamente"
        return response
    else:
        response.resultado = "error"
        return response

def curso_suscribir(request: suscribirCursoRequest, session, db: Session) -> defaultResponse:
    response: defaultResponse = defaultResponse()
    print(session["es_admin"])
    if session["es_admin"] is False:
        sub: SubTabla = db.query(SubTabla).filter(SubTabla.idusuario == session["idusuario"]).filter(SubTabla.idcurso == request.idcurso).first()
        if request.estado is True:
            if sub is not None:
                response.resultado = "error"
                response.mensaje = "Error al suscribirse a este curso"
                return response
            suscribir = SubTabla()
            suscribir.idusuario = session["idusuario"]
            suscribir.idcurso = request.idcurso
            db.add(suscribir)
            db.commit()
            response.resultado = "ok"
            response.mensaje = "suscrito a este curso correctamente"
            return response
        if request.estado is False:
            if sub is None:
                response.resultado = "error"
                response.mensaje = "error al desuscribirse del curso"
                return response
            db.delete(sub)
            db.commit()
            response.resultado = "ok"
            response.mensaje = "desuscrito correctamente"
            return response
    else:
        response.resultado = "error"
        response.mensaje = "ups... ocurrio un error inesperado"
        return response

def list_sub(session, db: Session) -> cursosResponse:
    response: cursosResponse = cursosResponse()
    if session["es_admin"] is False:
        sub: SubTabla = db.query(SubTabla).filter(SubTabla.idusuario == session["idusuario"]).all()
        if sub == []:
            response.resultado = "error"
            response.mensaje = "no tines suscripciones"
            return response
        cursos: List[curso] = []
        for suscripcion in sub:
            curso_tabla = db.query(CursoTabla).filter(CursoTabla.idcurso == suscripcion.idcurso).first()
            if curso_tabla is None:
                response.resultado = "error"
                response.mensaje = "no hay cursos para mostrar"
                return response
            i: curso = curso()
            i.idcurso = curso_tabla.idcurso
            i.titulo = curso_tabla.titulo
            i.descripcion = curso_tabla.descripcion
            cursos.append(i)
        response.resultado = "ok"
        response.cursos = cursos
        return response
    else:
        response.resultado = "error"
        return response