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

    query = Users.insert({Users.login: user.login, Users.password: user.password.get_secret_value(), Users.nickname: user.nickname})
    # isso acima equivale a : insert into users(login, password, nickname) values (user.login, user.password, user.nickname)
    _id = query.execute()

    return JSONResponse(
        {'Message': f'User created', 'id': _id}, 201
    )   # retorna o id pro broder


# 2- GET /user/{id}, que servirá para trazer informações do user que eu passar
@app.get('/user/{id}')
def get_user(id: int):

    user = Users.get_as_dict(Users.id == id)
    
    if user:
        del user['password']
        return JSONResponse({"User": user}, 200)

    return JSONResponse(
        {'Message': 'not found'}, 404
    )   # e retorna "not found"


# 3- PUT /user, que servirá para alterar algo do user (senha, login, nickname)

@app.put('/user/{id}') # decorador do PUT, que pega o id passado no path
def modify_user(id: int, modify_user: UserModify): # id que vem do path, modify_user que vem do payload

    user = Users.get_as_dict(Users.id == id)
    if not user:
        return JSONResponse({'Message': 'Not found'}, 404)    

    if modify_user.login: # se existir login no modify_user
        query = Users.update({Users.login: modify_user.login}).where(Users.id == id)
        query.execute()
        return JSONResponse({'Message': 'login modified'}) # retorna a resposta.

    if modify_user.password:
        query = Users.update({Users.password: modify_user.password}).where(Users.id == id)
        query.execute()
        return JSONResponse({'Message': 'password modified'})

    if modify_user.nickname:
        query = Users.update({Users.nickname: modify_user.nickname}).where(Users.id == id)
        query.execute()
        return JSONResponse({'Message': 'nickname modified'})

    return JSONResponse({"Message": "no field passed"}, 400)
    

@app.delete('/user/{id}')
def delete_user(id):

    query = Users.delete().where(Users.id == id)
    if query.execute():
        return JSONResponse({'Message': 'User Deleted'}, 200)

    return JSONResponse({'Message': 'Not found'}, 404)
