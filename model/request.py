from pydantic import BaseModel

class loginRequest(BaseModel):
    email: str
    password: str

class registerRequest(BaseModel):
    email: str
    password: str
    es_admin: bool

class crearCursoRequest(BaseModel):
    titulo: str
    descripcion: str

class suscribirCursoRequest(BaseModel):
    idcurso: int
    estado: bool #true para suscrito y false para desuscrito