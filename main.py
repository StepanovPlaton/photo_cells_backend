from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from Database.Database import DatabaseConnectionError, DatabaseBaseClass
from Routes import *
from Utils.Hasher import HasherClass
import os

app = FastAPI()
database = DatabaseBaseClass()
HasherObject = HasherClass()

if(not os.path.exists(os.path.join(".", "Content"))):
    os.mkdir(os.path.join(".", "Content"))
    os.mkdir(os.path.join(".", "Content", "full_size"))
    os.mkdir(os.path.join(".", "Content", "previews"))

@app.on_event("startup")  # type: ignore  
async def startup_server():
    if not await database.database_init():
        raise DatabaseConnectionError()


@app.on_event("shutdown")  # type: ignore
async def shutdown_server():
    await database.database_uninit()

app.mount("/static/", StaticFiles(directory="Content"), name="static")
app.include_router(Admin.router)
app.include_router(Images.router)
app.include_router(TagsAndSections.router)
