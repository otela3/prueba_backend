from typing import DefaultDict
import fastapi
import json
from database.database import SessionLocal
from database.models import UsuarioTabla
from model.response import defaultResponse, responseAutenticacion
from model.request import loginRequest, registerRequest
from sqlalchemy.orm import Session
from fastapi import Depends
from fastapi_jwt_auth import AuthJWT
from services import autenticar
from starlette.requests import Request
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
from starlette.responses import RedirectResponse

router = fastapi.APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post(
    path="/login",
    name="Login",
    description="Valida las credenciales de un usuario",
    response_model=responseAutenticacion
)
def login(request: loginRequest, db: Session = Depends(get_db), authorize: AuthJWT = Depends()):
    response: responseAutenticacion = autenticar.validarUsuario(request.email, request.password, db)
    if response.resultado == "error":
        return response
    
    sesion = {
        "idusuario": response.usuario.idusuario,
        "email": response.usuario.email,
        "es_admin": response.usuario.es_admin
    }
    response.resultado = "ok"
    response.mensaje = "usuario ingresado correctamente"
    response.token = authorize.create_access_token(subject=json.dumps(sesion), expires_time=False)
    return response


@router.post(
    path="/registrar/usuario",
    name="Registrar",
    description="Crea credenciales para un usuario",
    response_model=defaultResponse
)
def register(request: registerRequest, db: Session = Depends(get_db)):
    return autenticar.registrar(request, db)


config = Config('config.env')
oauth = OAuth(config)

CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
oauth.register(
    name='google',
    server_metadata_url=CONF_URL,
    client_kwargs={
        'scope': 'openid email profile'
    }
)

@router.get('/login/google')  # Tag it as "authentication" for our docs
async def login_google(request: Request):
    # Redirect Google OAuth back to our application
    redirect_uri = request.url_for('auth')
    
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.route('/auth')
async def auth(request: Request, db: Session = Depends(get_db), authorize: AuthJWT = Depends()):
    # Perform Google OAuth
    token = await oauth.google.authorize_access_token(request)
    user = await oauth.google.parse_id_token(request, token)

    # Save the user
    request.session['user'] = dict(user)
    return RedirectResponse(url='/google')

@router.get('/google')
async def home(request: Request, db: Session = Depends(get_db), authorize: AuthJWT = Depends()):
    user = request.session.get('user')
    
    if user is not None:
        usuario = request.session['user']
        usuarioTabla = db.query(UsuarioTabla).filter(UsuarioTabla.email == usuario['email']).first()
        if usuarioTabla is None:
            autenticar.registrarGoogle(usuario['email'], db)

        response: responseAutenticacion = autenticar.validarUsuarioGoogle(usuario['email'], "123", db)
        if response.resultado == "error":
            return response

        session = {
            "idusuario": response.usuario.idusuario,
            "email": response.usuario.email,
            "es_admin": response.usuario.es_admin
        }
        response.token = authorize.create_access_token(subject=json.dumps(session), expires_time=False)
        #token = autenticacion.tokenLogin("login")    
        return response.token

@router.get('/logout')  # Tag it as "authentication" for our docs
async def logout(request: Request):
    # Remove the user
    request.session.pop('user', None)

    return RedirectResponse(url='/')