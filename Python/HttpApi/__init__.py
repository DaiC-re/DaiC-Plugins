import DaiCCore
from fastapi import FastAPI

def init_server():
    app = FastAPI()

    @app.get("/")
    async def root():
        return {"message": "This is DaiC http server api"}

    @app.get("/get_str")
    async def get_str():
        return {"message": DaiCCore.get_str()}

DaiCCore.register("HttpApi", "DaiC http server api", init_server)

