from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class User(BaseModel):
    username: str
    email: str
    age: int


users = []


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/users", status_code=201)
def create_user(user: User):
    for existing_user in users:
        if existing_user.email == user.email:
            raise HTTPException(status_code=409, detail="Email already exists")

    users.append(user)
    return user


@app.get("/users/{username}")
def get_user(username: str):
    for user in users:
        if user.username == username:
            return user

    raise HTTPException(status_code=404, detail="User not found")


@app.post("/login")
def login(username: str, password: str):
    if username == "tester" and password == "test123":
        return {"message": "Login successful"}

    raise HTTPException(status_code=401, detail="Invalid credentials")
