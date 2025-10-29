## 🚀 Project Directories
- model
    - Contains the source code to deserialize or serialize input and output data
    - Contains the source code for project enums
    - Uses pydantics which comes with fastapi to validate data
- repositories
    - Contains the source code needed to query the database
    - Uses sqlalchemy orm library to interact with the data store
    - Asyncio is used for concurrency
- router (controller)
    - Contains the routing logic / source code for the API
- schema
    - Contains the source code for the data store structure
    - Uses sqlalchemy orm to talk to the data store and map or create structures
- services
    - Contains the source code for business logic / application logic
- sql
    - Contains sql source code to query database adhoc for dev

## 📦 Package Management
- pip

## 📨 Virtual Env
- venv

## 📦 Install Dependencies
```bash
pip install -r ./requirements.txt
```

## 📖 Libraries
1. fastapi
2. uvicorn
3. sqlalchemy
4. psycopg2-binary
5. asyncpg
6. bcrypt
7. greenlet
8. pytest
