import os

import uvicorn
from dotenv import load_dotenv

from fastapi import APIRouter, FastAPI
from fastapi.testclient import TestClient
from starlette.middleware.cors import CORSMiddleware

from src.api.routes.base import users, weather, covid
from src.api.routes.security import security

load_dotenv()
host = os.getenv('FASTAPI_HOST')
port = os.getenv('FASTAPI_PORT')
origins = ["*"]
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"])


@app.get("/")
def welcome_page():
    return {'msg': 'Hi from backend!'}


main_router = APIRouter()
main_router.include_router(users)
main_router.include_router(weather)
main_router.include_router(covid)
main_router.include_router(security, prefix='/security', tags=['Security'])

app.include_router(main_router)
client = TestClient(app)

if __name__ == '__main__':
    uvicorn.run('main:app',
                host=str(host),
                port=int(port),
                reload=True,
                timeout_keep_alive=0,
                log_level="info",
                use_colors=True)
