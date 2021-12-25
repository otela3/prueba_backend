from os import path
import fastapi
import json
from fastapi.params import Depends
from database.database import SessionLocal
from model.request import crearCursoRequest, suscribirCursoRequest
from model.response import defaultResponse, cursosResponse
from sqlalchemy.orm import Session
from fastapi_jwt_auth import AuthJWT
from services.cursoService import curso_crear, curso_listar, curso_eliminar, curso_suscribir, list_sub

router = fastapi.APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post(
    path="/crear/curso",
    name="crear curso",
    description="crea un curso",
    response_model=defaultResponse
)
def crear_curso(request: crearCursoRequest, db: Session = Depends(get_db), authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    session = json.loads(authorize.get_jwt_subject())
    return curso_crear(request, db, session)

@router.get(
    path="/cursos",
    name="Cursos",
    description="Lista Todos los Cursos",
    response_model=cursosResponse
)
def listar_cursos(db: Session = Depends(get_db), authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    session = json.loads(authorize.get_jwt_subject())
    return curso_listar(db)

@router.delete(
    path="/eliminar/curso/{id_curso}",
    name="eliminar curso",
    description="eliminar curso por id",
    response_model=defaultResponse
)
def eliminar_curso(id_curso: int, db: Session = Depends(get_db), authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    session = json.loads(authorize.get_jwt_subject())
    return curso_eliminar(id_curso, session, db)

@router.post(
    path="/suscribir/curso",
    name="suscribirse",
    description="permite a un usuario suscribirse y desuscribise a un curso",
    response_model=defaultResponse
)
def suscribir_curso(request: suscribirCursoRequest, db: Session = Depends(get_db), authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    session = json.loads(authorize.get_jwt_subject())
    return curso_suscribir(request, session, db)

@router.get(
    path="/suscribir/curso",
    name="lista sub cursos",
    description="lista de cursos a los que el usuario esta suscrito",
    response_model=cursosResponse
)
def sub_list(db: Session = Depends(get_db), authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    session = json.loads(authorize.get_jwt_subject())
    return list_sub(session, db)