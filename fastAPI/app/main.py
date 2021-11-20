import os
import sys
import uvicorn
from fastapi import FastAPI
import models
from database import engine

from routes import post, user, login, vote

# create Postgres Table(s)
models.Base.metadata.create_all(bind=engine)


app = FastAPI()

@app.get("/")
def root():
    """This is the homepage. This is used to test if the API is working correctly.
    """
    return {"msg": "Welcome! Your setup was correctly done."}

app.include_router(post.router)
app.include_router(user.router)
app.include_router(login.router)
app.include_router(vote.router)

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)
