from typing import DefaultDict, List
from pydantic import BaseModel

class defaultResponse(BaseModel):
    resultado: str = None
    mensaje: str = None

class dataUsuario(BaseModel):
    idusuario: int = None
    email: str = None
    es_admin: bool = None

    class Config:
        orm_mode=True

class responseAutenticacion(defaultResponse):
    usuario: dataUsuario = None
    token: str = None

class curso(BaseModel):
    idcurso: int = None
    titulo: str = None
    descripcion: str = None

class cursosResponse(defaultResponse):
    cursos: List[curso] = []
