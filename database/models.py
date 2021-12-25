from sqlalchemy import Column, Integer, String, Boolean
from database.database import Base


class UsuarioTabla(Base):
    __tablename__="usuario"

    idusuario = Column(Integer, primary_key=True)
    email = Column(String(200), nullable=False)
    password = Column(String(100), nullable=False)
    es_admin = Column(Boolean, nullable=False)

class CursoTabla(Base):
    __tablename__="curso"

    idcurso = Column(Integer, primary_key=True)
    titulo = Column(String(250))
    descripcion = Column(String(250))


class SubTabla(Base):
    __tablename__="sub"

    idusuario = Column(Integer, primary_key=True)
    idcurso = Column(Integer, primary_key=True)