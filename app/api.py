# app/api.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.database import collection
from bson import ObjectId


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
    "https://to-do-frontend-jet-two.vercel.app"  
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


@app.put("/todos/{id}", tags=["todos"])
async def update_todo(id: str, todo: TodoCreate):
    try:
        # ID string ko MongoDB ObjectId mein convert karo
        obj_id = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid Todo ID format")

    # Naye task text ko set karo
    update_data = {"$set": {"task": todo.task}}
    
    # Database mein find aur update karo
    update_result = await collection.find_one_and_update(
        {"_id": obj_id}, 
        update_data
    )

    if not update_result:
        # Agar uss ID ka todo nahi mila
        raise HTTPException(status_code=404, detail="Todo not found")

    # Updated todo ko database se dhoondho aur return karo
    updated_todo = await collection.find_one({"_id": obj_id})
    return todo_helper(updated_todo)


# DELETE Route: Ek todo ko delete karne ke liye
@app.delete("/todos/{id}", tags=["todos"])
async def delete_todo(id: str):
    try:
        # ID string ko MongoDB ObjectId mein convert karo
        obj_id = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid Todo ID format")

    # Database se find aur delete karo
    delete_result = await collection.find_one_and_delete({"_id": obj_id})

    if not delete_result:
        # Agar uss ID ka todo nahi mila
        raise HTTPException(status_code=404, detail="Todo not found")

    # '204 No Content' response bhej do (matlab success)
    return Response(status_code=204)