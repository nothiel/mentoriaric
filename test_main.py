import pytest
from starlette.testclient import TestClient
from fastapi import FastAPI
from pydantic import BaseModel, SecretStr
from starlette.responses import JSONResponse
from typing import Optional
from database import Users
from main import app

teste = TestClient(app)


def test_get_id_with_a_valid_id():
    expected_data = {
        'Usuario': {
            'login': 'ablulbe',
            'nickname': 'Azir Pelado',
            'id': '95698a41-b3dd-4855-923c-ac561ec8ec8b',
        }
    } #algo que esteja no banco

    response = teste.get('/user/95698a41-b3dd-4855-923c-ac561ec8ec8b')

    assert response.status_code == 200
    assert response.json() == expected_data

    # se o banco foi chamado (se o programa consultou algo no banco de dados)
    # se o tipo de dado que foi retornado é do mesmo tipo que o que eu espero
    # se o status code é o que eu desejei


def test_get_id_with_a_invalid_id():

    response = teste.get('/user/minhapica')
    # esperamos que retorna uma mensagem de "not found"
    # e o status code 404
    assert response.status_code == 404
    assert response.json() == {'Message': 'not found'}


def test_post_with_a_valid_payload():

    payload = {
        'login': 'juresbaldo666',
        'password': 'calcinhapreta',
        'nickname': 'estenometem23caracteres',
    }

    response = teste.post('/user', json=payload)
    response_json = response.json()
    assert (
        response_json['Message'] == 'User created'
    )   # que retorne uma mensagem de confirmação que foi gravado]
    assert response.status_code == 201   # e o status code 201
    assert len(response_json['id']) == 36   # e que foi gerado um id
    # esperamos que a aplicação grave os dados no banco


def test_post_with_a_invalid_payload():

    invalid_payload = {'lambe_minhas_bola': 'hahaha'}

    response = teste.post('/user', json=invalid_payload)
    response_json = response.json()

    assert response.status_code == 422
    

    # esperamos que ele não grave nada
    # esperamos o status code 422


def test_delete_with_a_valid_id():

    id = '95698a41-b3dd-4855-923c-ac561ec8ec8b' #algum valor que esteja no banco
    user = teste.get_as_dict(teste.id == id)
    if user:
        return JSONResponse({"User": user}, 200)
    # encontrar o id no banco
    assert user
    # asseguramos que isto está no banco

    # deletar essa linha que está o id
    response = teste.delete(f'/user/{id}')   # deletamos a linha disso no banco

    # assegurar que essa linha não existe mais
    assert not user

    # retornar status_code 200

    assert response.status_code == 200

    # exibir uma mensagem confirmando que foi deletado

    assert response.json() == {'Message': 'User Deleted'}


def test_delete_with_a_invalid_id():

    id = 'minhapica'

    # assegurar que ele não está no banco!
    user = teste.get_as_dict(teste.id == id)
 
    response = user.delete(f'/user/{id}')

    # status code == 404
    assert response.status_code == 404

    # mensagem = not found
    assert response.json() == {'Message': 'Not found'}



def test_put_with_a_valid_id():
    id = 'dc37dac7-9809-4c86-8ac9-070eb937d437' #algum id existente no banco

    # certificar que o id existe no banco
    user1 = teste.get_as_dict(teste.id == id)

    assert user1

    compare = user1

    # certificar que o campo que queremos foi alterado
    response = user1.put(f'/user/{id}', json={'login': 'valdinelson'})

    assert compare != response

    # certificar a exibição da mensagem de confirmação

    assert response.json() == {'Message': 'login modified'}

    # certificar o recebimento do status_code

    assert response.status_code == 200

def test_put_with_a_invalid_id():
    # certificar que id não está no banco
    id = 'joriscréudson'

    user = teste.get_as_dict(teste.id == id)

    assert not user

    response = user.put(f'/user/{id}', json={
        'login': 'fodasenvaiirmesmo'
    })
    # certificar exibição da mensagem de erro

    assert response.json() == {'Message': 'Not found'}
    # certificar 404

    assert response.status_code == 404