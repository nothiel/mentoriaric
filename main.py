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
        return JSONResponse({"Usuario": user}, 200)

    return JSONResponse(
        {'Message': 'not found'}, 404
    )   # e retorna "not found"


# 3- PUT /user, que servirá para alterar algo do user (senha, login, nickname)

@app.put('/user/{id}') # decorador do PUT, que pega o id passado no path
def modify_user(id: str, modify_user: UserModify): # id que vem do path, modify_user que vem do payload

    if modify_user.login: # se existir login no modify_user
        posi_line = return_line_position(id, 'banco.txt') # ele pega a posição da linha e a linha e coloca na variavel posi_line
        # primeira posição da posi_line: numero da linha no texto, ex: se for a segunda linha, posição 1
        # segunda posição da posi_line: é a string que estava na linha
        if posi_line: # se posi_line não for none, ou seja, se existir
            [position, line] = posi_line # desestrutura a lista para duas variaveis: position recebe a primeira posição da lista, line a segunda
            line = line.strip('\n').split(';') # cria uma lista de valores, separando-as pelo ; 
            line[1] = modify_user.login  # coloca o valor do login que recebemos na request no lugar do login que estava.
            new_line = ';'.join(line) # cria uma string dnv, juntando toda a lista com um ";"
            edit_line(position, 'banco.txt', new_line) #edita a linha que está na posição que foi encontrada no return_line_position
            return JSONResponse({'Message': 'login modified'}) # retorna a resposta.

    if modify_user.password:
        posi_line = return_line_position(id, 'banco.txt')
        if posi_line:
            [position, line] = posi_line
            line = line.strip('\n').split(';')
            line[2] = modify_user.password
            new_line = ';'.join(line)
            edit_line(position, 'banco.txt', new_line)
            return JSONResponse({'Message': 'password modified'})

    if modify_user.nickname:
        posi_line = return_line_position(id, 'banco.txt')
        if posi_line:
            [position, line] = posi_line
            line = line.strip('\n').split(';')
            line[3] = modify_user.nickname
            new_line = ';'.join(line)
            edit_line(position, 'banco.txt', new_line)
            return JSONResponse({'Message': 'nickname modified'})

    return JSONResponse({'Message': 'Not found'}, 404)


def return_line_position(id, filename):

    with open(filename, 'r') as file:
        for index, line in enumerate(file):
            line = line.strip('\n')
            idbanco = line.split(';')[0]
            if id == idbanco:
                return index, line


def edit_line(position, filename, new_line):

    with open(filename, 'r') as file:
        all_lines = file.readlines()

    with open(filename, 'w') as file:
        all_lines[position] = new_line

        file.write(''.join(all_lines))


def delete_line(position, filename):

    with open(filename, 'r') as file:
        all_lines = file.readlines()

    with open(filename, 'w') as file:
        del all_lines[position]

        file.write('\n'.join(all_lines))


@app.delete('/user/{id}')
def delete_user(id):
    line_posi = return_line_position(id, 'banco.txt')
    if line_posi:
        [position, _] = line_posi
        delete_line(position, 'banco.txt')
        return JSONResponse({'Message': 'User Deleted'}, 200)

    return JSONResponse({'Message': 'Not found'}, 404)
