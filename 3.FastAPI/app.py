from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI(title="My first API")


class Task(BaseModel):
    task: str
    description: str | None = None
    done: bool | None = False


@app.get("/")
def root():
    return {"message": "Hello from FastAPI"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/add")
def add(a: int, b: int):
    return {"result": a + b}


@app.get("/hello/{name}")
def max(name: str):
    return {"hello": name}


@app.post("/tasks", status_code=201)
def create_task(task: Task):
    return task

