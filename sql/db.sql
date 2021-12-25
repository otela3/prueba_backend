DROP DATABASE IF EXISTS puebadb;
CREATE DATABASE pruebadb;
\c pruebadb;

\echo 'LOADING databse'

CREATE TABLE "usuario"
(
  idusuario SERIAL PRIMARY KEY,
  email VARCHAR(200) NOT NULL,
  password VARCHAR(100) NOT NULL,
  es_admin BOOLEAN NOT NULL
);
CREATE TABLE "curso"
(  
  idcurso SERIAL PRIMARY KEY,
  titulo VARCHAR(250),
  descripcion VARCHAR(250)
);
CREATE TABLE "sub"
(
  idusuario INTEGER,
  idcurso INTEGER,
  PRIMARY KEY(idusuario, idcurso)
);
