from fastapi import FastAPI, Request
import uvicorn
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from models import User

app = FastAPI()
templates = Jinja2Templates(directory="templates")

users = []

@app.get("/users", response_class=HTMLResponse)
async def read_users(request: Request):
    return templates.TemplateResponse("users.html", {"request": request, "users": users})


@app.get("/create_new_user", response_class=HTMLResponse)
def create_new_user(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@app.post("/add_user")
async def add_user(user: User):
    users.append(user)


@app.get("/")
def root():
    return RedirectResponse("/users")


if __name__ == "__main__":
    users.append(User(name='Alex', email='test@gmail.com', password='323547y3wqgehw'))
    users.append(User(name='Mary', email='mary@gmail.com', password='rhgrjtrhegwfh'))
    users.append(User(name='Joe', email='joe@gmail.com', password='ehjkyjthreg'))
    uvicorn.run(app, host="127.0.0.1", port=8000)