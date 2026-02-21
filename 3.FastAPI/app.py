from abc import ABC, abstractmethod
from fastapi import Depends, FastAPI, HTTPException, Response
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



class Storage(ABC):
    @abstractmethod
    def create(self, data: TaskCreate) -> TaskOut:
        ...

    @abstractmethod
    def get(self, task_id: int) -> TaskOut:
        ...

    @abstractmethod
    def list(self) -> list[TaskOut]:
        ...

    @abstractmethod
    def delete(task_id: int) -> bool:
        ...


class InMemoryStorage(Storage):
    def __init__(self):
        self.tasks_db: dict[int, TaskOut] = {}
        self.next_id = 1

    def create(self, data: TaskCreate) -> TaskOut:
        new_task = TaskOut(id=self.next_id, **data.model_dump())
        self.tasks_db[self.next_id] = new_task
        self.next_id += 1
        return new_task

    def get(self, task_id: int) -> TaskOut:
        return self.tasks_db.get(task_id)

    def list(self) -> list[TaskOut]:
        return list(self.tasks_db.values())

    def delete(self, task_id: int) -> bool:
        if task_id in self.tasks_db:
            del self.tasks_db[task_id]
            return True
        return False

    def save(self, task: TaskOut) -> TaskOut:
        try:
            self.tasks_db[task.id] = task
        except KeyError:
            return False
        return True



storage = InMemoryStorage()

def get_storage() -> Storage:
    return storage



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
def create_task(task: TaskCreate, storage: Storage = Depends(get_storage)):
    new_task = storage.create(task)
    return new_task


@app.get("/tasks", response_model=list[TaskOut])
def list_tasks(done: bool | None = None, storage: Storage = Depends(get_storage)):
    all_tasks = storage.list()
    if done is None:
        return all_tasks
    return [task for task in all_tasks if task.done == done]


@app.get("/tasks/{task_id}", response_model=TaskOut)
def get_task(task_id: int, storage: Storage = Depends(get_storage)):
    task = storage.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int, storage: Storage = Depends(get_storage)):
    if not storage.delete(task_id):
        raise HTTPException(status_code=404, detail="Task not found")
    return Response(status_code=204)


@app.patch("/tasks/{task_id}", response_model=TaskOut)
def patch_task(task_id: int, patch: TaskUpdate, storage: Storage = Depends(get_storage)):
    task = storage.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    updates = patch.model_dump(exclude_unset=True)
    updated_task = task.model_copy(update=updates)
    if not storage.save(updated_task):
        raise HTTPException(status_code=500, detail="Can not save the task")
    return updated_task


@app.put("/tasks/{task_id}", response_model=TaskOut)
def replace_task(task_id: int, new_task: TaskCreate, storage: Storage = Depends(get_storage)):
    task = storage.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    updates = new_task.model_dump()
    updated_task = task.model_copy(update=updates)
    if not storage.save(updated_task):
        raise HTTPException(status_code=500, detail="Can not save the task")
    return updated_task

