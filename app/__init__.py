import os
import mongoengine
from fastapi import FastAPI
from importlib import import_module
from fastapi.middleware.cors import CORSMiddleware

from utils.logger import console_logger


def add_routers(app):
    # including routers in the app
    from app.users.routes import router as user_router
    app.include_router(user_router, prefix="/api")

def dbinit():
    # initializing database
    mongoengine.connect(
        db="UsersDB", 
        host='mongo', 
        username='root', 
        password='example', 
        authentication_source='admin'
    )

def init_middleware(app):
    # cors middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

def create_app():
    # app 
    app = FastAPI(
        title="Users CRUD API",
        version="1.0.0",
    )

    # initializing middleware
    init_middleware(app)

    # initializing db
    dbinit()

    # add routers
    add_routers(app)

    return app

app = create_app()
