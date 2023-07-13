import enum
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from starlette.responses import RedirectResponse


class Status(enum.Enum):
    todo = 0
    in_progress = 1
    done = 2


class Task(BaseModel):
    id: int
    title: str
    description: str
    status: Status


class TaskInput(BaseModel):
    title: str
    description: str
    status: Status


tasks = []

app = FastAPI()


@app.get("/tasks", response_model=list[Task])
def get_tasks():
    return tasks


@app.post("/tasks", response_model=list[Task])
def new_task(task: TaskInput):
    task = Task(
        id=len(tasks) + 1,
        title=task.title,
        description=task.description,
        status=task.status
    )
    tasks.append(task)
    return tasks


@app.put("/tasks/{task_id}", response_model=TaskInput)
def edit_task(task_id: int, new_task: Task):
    for task in tasks:
        if task.id == task_id:
            task.title = new_task.title
            task.description = new_task.description
            task.status = new_task.status
            return task
    raise HTTPException(status_code=404, detail="Task not found")


@app.delete("/tasks/{task_id}", response_model=str)
def delete_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            tasks.remove(task)
            return "task was deleted"
    raise HTTPException(status_code=404, detail="Task not found")


@app.get("/")
def root():
    return RedirectResponse("/tasks")


if __name__ == '__main__':
    for i in range(10):
        tasks.append(Task(id=i, title=f"title{i}",
                          description=f"description{i}",
                          status=Status.todo))

    uvicorn.run(app, host="127.0.0.1", port=8000)