from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from enum import Enum
import uuid
import os
from databases import Database  # New import for database connection

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TodoStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"

class Todo(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    status: TodoStatus = TodoStatus.PENDING

class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = None

DATABASE_URL = os.getenv("DATABASE_URL")  # Get database URL from environment variables
print("dbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb")
print(DATABASE_URL)
print("dbbbbbbbbb")
database = Database(DATABASE_URL)  # Create a database connection

@app.on_event("startup")
async def startup():
    await database.connect()  # Connect to the database

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()  # Disconnect from the database

@app.post("/todos/", response_model=Todo)
async def create_todo(todo: TodoCreate):
    todo_id = str(uuid.uuid4())
    todo_dict = todo.model_dump()
    new_todo = Todo(id=todo_id, **todo_dict)
    query = "INSERT INTO todos (id, title, description, status) VALUES (:id, :title, :description, :status)"
    await database.execute(query, values={"id": todo_id, "title": new_todo.title, "description": new_todo.description, "status": new_todo.status})
    return new_todo

@app.get("/todos/", response_model=List[Todo])
async def list_todos():
    query = "SELECT * FROM todos"
    rows = await database.fetch_all(query)
    return [Todo(**row) for row in rows]

@app.get("/todos/{todo_id}", response_model=Todo)
async def get_todo(todo_id: str):
    query = "SELECT * FROM todos WHERE id = :id"
    row = await database.fetch_one(query, values={"id": todo_id})
    if row is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return Todo(**row)

@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: str):
    query = "DELETE FROM todos WHERE id = :id"
    result = await database.execute(query, values={"id": todo_id})
    if result == 0:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"message": "Todo deleted successfully"}

@app.put("/todos/{todo_id}/complete", response_model=Todo)
async def complete_todo(todo_id: str):
    query = "UPDATE todos SET status = :status WHERE id = :id"
    result = await database.execute(query, values={"status": TodoStatus.COMPLETED, "id": todo_id})
    if result == 0:
        raise HTTPException(status_code=404, detail="Todo not found")
    return await get_todo(todo_id)  # Return the updated todo

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=54439)
