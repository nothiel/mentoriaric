from fastapi import FastAPI
from pydantic import BaseModel, SecretStr
from starlette.responses import JSONResponse
from typing import Optional
from database import Users


app = FastAPI()


@app.get('/')
def root():
    return {'Hello': 'World!'}


# Quero criar uma API, onde ela terá quatro rotas:


class User(BaseModel):
    login: str
    password: SecretStr
    nickname: str


class UserModify(BaseModel):
    login: Optional[str]
    password: Optional[str]
    nickname: Optional[str]


# 1- POST /user, que servirá para registrar um novo usuário


@app.post('/user')
def create_user(user: User):   # cria função para criar usuario,

    query = Users.insert({Users.login: user.login, Users.password: user.password, Users.nickname: user.nickname}) 
    # isso acima equivale a : insert into users(login, password, nickaname) values (user.login, user.password, user.nickname)
    id = query.execute()

    return JSONResponse(
        {'Message': f'User created', 'id': str(id)}, 201
    )   # retorna o id pro broder


# 2- GET /user/{id}, que servirá para trazer informações do user que eu passar
@app.get('/user/{id}')
def get_user(id: int):

    user = Users.get_as_dict(Users.id == id)
    if user:
        return JSONResponse({"User": user}, 200)

    return JSONResponse(
        {'Message': 'not found'}, 404
    )   # e retorna "not found"


# 3- PUT /user, que servirá para alterar algo do user (senha, login, nickname)

@app.put('/user/{id}') # decorador do PUT, que pega o id passado no path
def modify_user(id: int, user: User): #id do tipo int e user do tipo User

    user = Users.get_as_dict(Users.id == id)

    if user:
            query = Users.update({Users.login: user.login, Users.password: user.password, Users.nickname: user.nickname}) 
    # isso acima equivale a : update into users(login, password, nickaname) values (user.login, user.password, user.nickname)
            id = query.execute()
            return JSONResponse({"User changed": user}, 200)
    return JSONResponse({'Message': 'Not found'}, 404)

@app.delete('/user/{id}')
def delete_user(id: int, user: User):
    user = Users.get_as_dict(Users.id == id)

    if user:
        query = Users.delete({Users.login: user.login, Users.password: user.password, Users.nickname: user.nickname}) 
    # isso acima equivale a : delete users(login, password, nickaname) values (user.login, user.password, user.nickname)
        return JSONResponse({'Message': 'User Deleted'}, 200)

    return JSONResponse({'Message': 'Not found'}, 404)
