from fastapi import FastAPI

from app.main.bootstrap import configure_app, create_app
from app.presentation.http.controllers.root_router import root_router


def make_app() -> FastAPI:
    app = create_app()
    configure_app(app=app, root_router=root_router)
    return app


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app=make_app(),
        port=8000,
        reload=False,
    )
