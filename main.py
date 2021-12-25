import fastapi
import uvicorn
from api import autenticacion, curso
from pydantic import BaseModel
from fastapi_jwt_auth import AuthJWT
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware

tags_metadata = [
    {
        "name": "Autenticación",
        "description": "Para muchos EP será necesario contar con token de acceso."
    },
]

api = fastapi.FastAPI(
    title="Prueba Backend",
    description="API REST Prueba Backend",
    version="0.1",
    openapi_tags=tags_metadata
)

api.add_middleware(SessionMiddleware, secret_key='!secret')

api.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],  # PARA SERVER DESARROLLO
    allow_credentials = False,  # PARA SERVER DESARROLLO
    allow_methods = ["*"],  # PARA SERVER DESARROLLO
    allow_headers=["*"])

class Settings(BaseModel):
    authjwt_secret_key: str = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJPbmxpbmUgSldUIEJ1aWxkZXIiLCJpYXQiOjE2MjMwMDU4ODksImV4cCI6MTY1NDU0MTg4OSwiYXVkIjoid3d3LmV4YW1wbGUuY29tIiwic3ViIjoianJvY2tldEBleGFtcGxlLmNvbSIsIkdpdmVuTmFtZSI6IkpvaG5ueSIsIlN1cm5hbWUiOiJSb2NrZXQiLCJFbWFpbCI6Impyb2NrZXRAZXhhbXBsZS5jb20iLCJSb2xlIjpbIk1hbmFnZXIiLCJQcm9qZWN0IEFkbWluaXN0cmF0b3IiXX0.J3kj115YOHzQeqyqP7_9LV7ItquNr3spUUQhB3nZSRY"


@AuthJWT.load_config
def get_config():
    return Settings()

def configure():
    api.include_router(autenticacion.router, tags=["Autenticación"])
    api.include_router(curso.router, tags=["Curso"])

configure()

if __name__ == '__main__':
    uvicorn.run("main:api", host="127.0.0.1", port=8000, reload=True)