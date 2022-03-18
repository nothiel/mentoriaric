import pytest
from starlette.testclient import TestClient
from database import Users
from main import app

teste = TestClient(app)


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
    assert isinstance(response_json['id'], int)   # e que foi gerado um id
    assert Users.get_as_dict(Users.id == response_json['id'])


def test_post_with_a_invalid_payload():

    invalid_payload = {'lambe_minhas_bola': 'hahaha'}

    response = teste.post('/user', json=invalid_payload)

    assert response.status_code == 422

    # esperamos o status code 422

def test_get_id_with_a_valid_id():

    response = teste.get('/user/1')

    assert response.status_code == 200
    assert 'User' in response.json()

    # se o banco foi chamado (se o programa consultou algo no banco de dados)
    # se o tipo de dado que foi retornado é do mesmo tipo que o que eu espero
    # se o status code é o que eu desejei


def test_get_id_with_a_invalid_id():

    response = teste.get('/user/9000')
    # esperamos que retorna uma mensagem de "not found"
    # e o status code 404
    assert response.status_code == 404
    assert response.json() == {'Message': 'not found'}


def test_put_with_a_valid_id():
    _id = 1

    # certificar que o id existe no banco
    user = Users.get_as_dict(Users.id == _id)

    assert user

    response = teste.put(f'/user/{_id}', json={
        'login': 'valdinelson'
    })

    assert user != Users.get_as_dict(Users.id == _id)
    # certificar a exibição da mensagem de confirmação

    assert response.json() == {'Message': 'login modified'}

    # certificar o recebimento do status_code

    assert response.status_code == 200

def test_put_with_a_invalid_id():
    # certificar que id não está no banco
    _id = 1239234324

    assert not Users.get_as_dict(Users.id == _id)

    response = teste.put(f'/user/{_id}', json={
        'login': 'fodasenvaiirmesmo'
    })
    # certificar exibição da mensagem de erro

    assert response.json() == {'Message': 'Not found'}
    # certificar 404

    assert response.status_code == 404




def test_delete_with_a_valid_id():

    _id = 1

    assert Users.get_as_dict(Users.id == _id)

    response = teste.delete(f'/user/{_id}')   # deletamos a linha disso no banco

    assert not Users.get_as_dict(Users.id == _id)

    # retornar status_code 200

    assert response.status_code == 200

    # exibir uma mensagem confirmando que foi deletado

    assert response.json() == {'Message': 'User Deleted'}


def test_delete_with_a_invalid_id():

    _id = 100000000

    # assegurar que ele não está no banco!
    assert not Users.get_as_dict(Users.id == _id)

    response = teste.delete(f'/user/{_id}')

    # status code == 404
    assert response.status_code == 404

    # mensagem = not found
    assert response.json() == {'Message': 'Not found'}