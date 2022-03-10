import uuid
from click import edit
from fastapi import FastAPI
from pydantic import BaseModel, SecretStr
from starlette.responses import JSONResponse
from typing import Optional
import in_place


app = FastAPI()


@app.get('/')
def root():
    return {"Hello": "World!"}

# Quero criar uma API, onde ela terá quatro rotas:

class User(BaseModel):
    login: str
    password: SecretStr
    nickname: str

class UserModify(BaseModel):
    login: Optional[str]
    password: Optional[SecretStr]
    nickname: Optional[str]

# 1- POST /user, que servirá para registrar um novo usuário

@app.post('/user')
def create_user(user: User):
    id = uuid.uuid4()
    # Adicionar um usuario com senha, login, e nickname no arquivo de texto no seguinte padrão:
    # id;login;senha;nickname
    file_line = f'{id};{user.login};{user.password.get_secret_value()};{user.nickname}\n' # isso não é uma boa pratica
    
    fout = open('banco.txt', 'a')

    fout.write(file_line)
    fout.close()
    # em seguida, retornar o ID do usuario na mensagem

    return JSONResponse({"Mesage": f"User created. ID: {id}"}, 201)


# 2- GET /user/{id}, que servirá para trazer informações do user que eu passar
@app.get('/user/{id}')
def get_user(id: str):

    fin = open('banco.txt', 'r')
    for line in fin:
        line = line.strip('\n')
        [id_banco, login, _, nickname] = line.split(';')
        if id == id_banco:
            fin.close()
            return JSONResponse({'Usuario': {'id': id, 'login': login, 'nickname': nickname}}, 200)
    fin.close()
    return JSONResponse({"Message": "not found"}, 404)
    

# 3- PUT /user, que servirá para alterar algo do user (senha, login, nickname)

@app.put('/user/{id}')
def modify_user(id : str, modify_user: UserModify):


    if modify_user.login:
        posi_line = return_line_position(id, 'banco.txt')
        if posi_line:
            [position, line] = posi_line
            line = line.strip('\n').split(';')
            line[1] = modify_user.login
            new_line = ';'.join(line)
            edit_line(position, 'banco.txt', new_line)
            return JSONResponse({"Message": "login modified"})

    if modify_user.password:
        posi_line = return_line_position(id, 'banco.txt')
        if posi_line:
            [position, line] = posi_line
            line = line.strip('\n').split(';')
            line[2] = modify_user.password
            new_line = ';'.join(line)
            edit_line(position, 'banco.txt', new_line)
            return JSONResponse({"Message": "password modified"})

    if modify_user.nickname:
        posi_line = return_line_position(id, 'banco.txt')
        if posi_line:
            [position, line] = posi_line
            line = line.strip('\n').split(';')
            line[3] = modify_user.nickname
            new_line = ';'.join(line)
            edit_line(position, 'banco.txt', new_line)
            return JSONResponse({"Message": "nickname modified"})

    print(modify_user.login)

    return JSONResponse({"Message":"Not found"}, 404)


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

        file.write('\n'.join(all_lines))


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
        return JSONResponse({"Message":"User Deleted"}, 200)

    return JSONResponse({"Message":"Not found"}, 404)

    
