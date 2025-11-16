# app/api.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.database import collection

# --- Pydantic Model
class TodoCreate(BaseModel):
    task: str

# --- Helper Function [ which converts MongoDB document to dict ]
def todo_helper(todo) -> dict:
    return {
        "id": str(todo["_id"]),
        "task": todo["task"],
    }


app = FastAPI()

origins = [
    "http://localhost:5173",
    "localhost:5173",
    "httpsS://todo-app-frontend.vercel.app"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)



# GET Route:get all todos 
@app.get("/todos", tags=["todos"])
async def get_todos():
    todos = []

    async for todo in collection.find():
        todos.append(todo_helper(todo))
    return todos

# POST Route: create a todo
@app.post("/todos", tags=["todos"])
async def create_todo(todo: TodoCreate):
    todo_data = todo.model_dump() 
    
   
    new_todo = await collection.insert_one(todo_data)
    
    
    created_todo = await collection.find_one({"_id": new_todo.inserted_id})
    

    return todo_helper(created_todo)