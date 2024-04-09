from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from typing import List
from bson import ObjectId
from dotenv import load_dotenv
import os
from fastapi.responses import Response

app = FastAPI()

# MongoDB connection URL
MONGO_URL = os.getenv('MONGO_URI')

client = AsyncIOMotorClient(MONGO_URL)
database = client["library"]


# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You have successfully connected to MongoDB!")
except Exception as e:
    print(e)


class Address(BaseModel):
    city: str
    country: str

class Student(BaseModel):
    name: str
    age: int
    address: Address

@app.post('/students/' , status_code=201)
async def create_student(student: Student):
    if database is None:
        raise HTTPException(status_code=500, detail="Database connection not established")
    collection = database["students"]
    try:
        student = student.dict()
        print(student)
        result = await collection.insert_one(student)
        print(result)
        if result.inserted_id:
            # Update the student object with the inserted ID
            print(result.inserted_id)
            id = str(result.inserted_id)
            print(id)
            return {"id": id, "message": "Student created successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to insert student into database")    
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while creating the student")
    

@app.get('/students', status_code=200)
async def list_students(country: str = None, age: int = None):
    collection = database["students"]
    query = {}
    if country:
        query["address.country"] = country
    if age is not None:
        query["age"] = {"$gte" : age}    
    students = await collection.find(query).to_list(None)
    listStudents = [{"name": st["name"], "age": st["age"]} for st in students]
    return {
        "data" : listStudents
    }        


@app.get("/students/{id}", status_code=200)
async def get_student_by_id(id: str):
    collection = database["students"]
    student = await collection.find_one({"_id":ObjectId(id)})
    if student:
        del student["_id"]
        return student
    raise HTTPException(status_code=404, detail="Student Not found")


@app.patch("/students/{id}", status_code=204)
async def update_student(id: str, changes: dict):
    collection = database["students"]
    try:
        object_id = ObjectId(id)
    except:
        raise HTTPException(status_code=400, detail="Invalid ID")

    if "_id" in changes:
        del changes["_id"]  
    update_student_data = {"$set": changes}  
    result = await collection.update_one({"_id": object_id}, update_student_data)    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")  
    return {}    

@app.delete("/students/{id}", status_code=200)
async def delete_student(id: str):
    collection = database["students"]
    deleted_item = await collection.find_one_and_delete({"_id": ObjectId(id)})
    if deleted_item:
        return {}
    raise HTTPException(status_code=404, detail="student not found")



