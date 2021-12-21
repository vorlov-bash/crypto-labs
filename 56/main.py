import uvicorn
from fastapi import FastAPI

from injector import MainContainer
from config import CONFIG

container = MainContainer()


def init_v1_app():
    from v1.routes import user, to_inject

    container.wire(modules=[*to_inject])

    sql_lite_proxy = container.v1.gateways.sqlite()

    app = FastAPI()
    app.include_router(user.router)

    @app.on_event("startup")
    async def startup():
        await sql_lite_proxy.run_create_all()

    return app


def run_v1_app():
    uvicorn.run('main:init_v1_app', host=CONFIG.v1.host, port=CONFIG.v1.port)


if __name__ == '__main__':
    if CONFIG.version == 'v1':
        uvicorn.run(init_v1_app(), host=CONFIG.v1.host, port=CONFIG.v1.port)

