# Library management FastAPI

Created a Backend API using 
1. FastAPI
2. mongoDB
3. MOTOR
4. pydantic
5. deployed using docker image to render platform

**To test locally:**
  1. Clone the repository
  2. Add your MongoDb url from the mongodb atlas to .env (create it locally) MONGO_URI = your connection string.
  3. build the docker file with `docker build -t <my-app-name> .`
  4. run docker image -  `docker run -p 8000:8000 --env-file .env <my-app-name>`
  5. Replace the my-app-name with the name you want or just remove <>
  6. The server is running , check on POSTMAN , by replacing the     localhost:8000 , in below url.


**The render url:** `https://library-management-backend-api-python.onrender.com/` 

## The endpoints for API

### 1. Add a new student
- **URL:** `https://library-management-backend-api-python.onrender.com/students/`
- **Method:** `POST`
- **Request Body:** status_code - `201`
    ```json
    {
        "name": "Abhishek Singh",
        "age": 24,
        "address": {
            "city": "Hyderabad",
            "country": "India"
        }
        
    }
    ```
- **Response:**
    ```json
    {
        "id": "6615308475578a731660a361",
        "message": "Student created successfully"
    }
    ```


### 2. List students with optional filter as query params for age and country (gets all with age>=given_age and have the country)
- **URL:** `/api/students/`
- **Method:** `GET`
- **Query students**: `https://library-management-backend-api-python.onrender.com/students?country=India&age=20`
- **Response body:** status_code - `200`
    ```json
    {
        "data" : [
            {
               "name": "Rajat",
                "age": 25
            },
            {
               "name": "Abhishek",
                "age": 24
            }
        ]
    }
    ```

### 3. Get student by ID
- **URL:** `https://library-management-backend-api-python.onrender.com/students/{id}`  (Example id = 6615308475578a731660a361)
- **Method:** `GET`

- **Response body:** status_code - `200`
    ```json
    {
        "name": "Abhishek Singh",
        "age": 26,
        "address": {
            "city": "Hyderabad",
            "country": "India"
        }
    }
    ```

### 4. Make changes by ID
- **URL:** `https://library-management-backend-api-python.onrender.com/students/{id}` (Example id = 6615308475578a731660a361)
- **Method:** `PATCH`
- **Request Body:** This will change the name and age to the given id
    ```json
    {
        "name": "Abhishek",
        "age": 24
        
    }
    ```
- **Response Body:** status_code - `204`
    ```json
    {}
    ```


### 5. Delete student by ID
- **URL:** `https://library-management-backend-api-python.onrender.com/students/{id}` (Example id = 6615308475578a731660a361)
- **Method:** `DELETE`

- **ResponseBody:** status_code - `200`
    ```json
    {}
    ```