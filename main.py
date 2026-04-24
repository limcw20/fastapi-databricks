from fastapi import FastAPI
from routes import users
from db.connection import db_manager

app = FastAPI()

app.include_router(users.router, prefix="/users")



@app.on_event("shutdown")
async def shutdown():
    db_manager.close()