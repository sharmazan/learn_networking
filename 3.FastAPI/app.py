from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel


app = FastAPI(title="My first API")


class TaskCreate(BaseModel):
    name: str
    description: str | None = None
    done: bool = False


class TaskOut(TaskCreate):
    id: int


class TaskUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    done: bool | None = None


tasks_db: dict[int, TaskOut] = {}
next_id = 1


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
def hello(name: str):
    return {"hello": name}


@app.post("/tasks", status_code=201, response_model=TaskOut)
def create_task(task: TaskCreate):
    global next_id

    new_task = TaskOut(id=next_id, **task.model_dump())
    tasks_db[next_id] = new_task
    next_id += 1
    return new_task


@app.get("/tasks", response_model=list[TaskOut])
def list_tasks():
    return list(tasks_db.values())


@app.get("/tasks/{task_id}", response_model=TaskOut)
def get_task(task_id: int):
    task = tasks_db.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    try:
        del tasks_db[task_id]
    except KeyError:
        raise HTTPException(status_code=404, detail="Task not found")
    return Response(status_code=204)


@app.patch("/tasks/{task_id}", response_model=TaskOut)
def update_task(task_id: int, patch: TaskUpdate):
    try:
        task = tasks_db[task_id]
    except KeyError:
        raise HTTPException(status_code=404, detail="Task not found")
    updates = patch.model_dump(exclude_unset=True)
    updated_task = task.model_copy(update=updates)
    tasks_db[task_id] = updated_task
    return updated_task


@app.put("/tasks/{task_id}", response_model=TaskOut)
def replace_task(task_id: int, new_task: TaskCreate):
    task = tasks_db.get(task_id)
    if task is None:
        raise HTTPExcept(status_code=404, detail="Task not found")
    updates = new_task.model_dump()
    updated_task = task.model_copy(update=updates)
    tasks_db[task_id] = updated_task
    return updated_task

