import uvicorn

from fastapi import APIRouter, FastAPI
from fastapi.testclient import TestClient
from starlette.middleware.cors import CORSMiddleware

from cfg import api_host, api_port
from src.api.routes.base import users, weather, covid
from src.api.routes.security import security

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
                host=str(api_host),
                port=int(api_port),
                reload=True,
                timeout_keep_alive=0,
                log_level="info",
                use_colors=True)
