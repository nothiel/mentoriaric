from fastapi import FastAPI
from starlette.responses import JSONResponse

from database import Users
from models import User, UserModify
from service import checkapass, create, delete, read, update
from utils import hashpw

app = FastAPI()


@app.get('/')
def root():
    return {'Hello': 'World!'}


@app.post('/user')
def create_user(user: User):
    user = hashpw(user)
    _id = create(user.dict())

    return JSONResponse({'Message': f'User created', 'id': _id}, 201)


@app.get('/user/{id}')
def get_user(id: int):

    user = read(id)
    
    if not user:
        return JSONResponse({'Message': 'not found'}, 404)

    return JSONResponse({"User": user}, 200)


# 3- PUT /user, que servirá para alterar algo do user (senha, login, nickname)

@app.put('/user/{id}') # decorador do PUT, que pega o id passado no path
def modify_user(id: int, modify_user: UserModify): # id que vem do path, modify_user que vem do payload

    if not update(modify_user, id):
        return JSONResponse({'Message': 'Not found'}, 404)

    return JSONResponse({'Message': 'User Modified'}, 200)

@app.delete('/user/{id}')
def delete_user(id):

    if not delete(id):
        return JSONResponse({'Message': 'Not found'}, 404)
    return JSONResponse({'Message': 'User Deleted'}, 200)


@app.post('/login')
def authenticate(user: dict):
    return checkapass(user)