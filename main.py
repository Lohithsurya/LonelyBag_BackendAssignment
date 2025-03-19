from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional, Dict
import uvicorn

# Create FastAPI instance
app = FastAPI(title="User Management API")

# Pydantic model for User
class User(BaseModel):
    id: int
    name: str
    phone_no: str
    address: str

# Pydantic model for updating User
class UserUpdate(BaseModel):
    name: str
    phone_no: str
    address: str

# In-memory storage for users
users_db: Dict[int, User] = {}

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to the User Management API",
        "endpoints": {
            "Create user": "POST /users/",
            "Get user by ID": "GET /users/{user_id}",
            "Search users by name": "GET /users/search?name={name}",
            "Update user": "PUT /users/{user_id}",
            "Delete user": "DELETE /users/{user_id}",
            "API documentation": "/docs or /redoc"
        }
    }

# Create a new user
@app.post("/users/", status_code=201)
async def create_user(user: User):
    if user.id in users_db:
        raise HTTPException(status_code=400, detail="User with this ID already exists")
    users_db[user.id] = user
    return {"message": "User created successfully"}

# Read user by id
@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    return users_db[user_id]

# Read users by name
@app.get("/users/search", response_model=List[User])
async def search_users(name: str = Query(..., description="Name to search for")):
    matched_users = [user for user in users_db.values() if name.lower() in user.name.lower()]
    return matched_users

# Update user details
@app.put("/users/{user_id}")
async def update_user(user_id: int, user_update: UserUpdate):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update user while preserving the id
    current_user = users_db[user_id]
    updated_user = User(
        id=user_id,
        name=user_update.name,
        phone_no=user_update.phone_no,
        address=user_update.address
    )
    users_db[user_id] = updated_user
    
    return {"message": "User updated successfully"}

# Delete user by id
@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    del users_db[user_id]
    return {"message": "User deleted successfully"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)