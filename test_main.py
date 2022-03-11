import pytest
from starlette.testclient import TestClient
from main import app, return_line_position

teste = TestClient(app)


def test_get_id_with_a_valid_id():
    expected_data = {
        'Usuario': {
            'login': 'ablulbe',
            'nickname': 'Azir Pelado',
            'id': '95698a41-b3dd-4855-923c-ac561ec8ec8b',
        }
    }

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
    assert return_line_position(
        response_json['id'], 'banco.txt'
    )   # esperamos que a aplicação grave os dados no banco


def test_post_with_a_invalid_payload():

    invalid_payload = {'lambe_minhas_bola': 'hahaha'}

    response = teste.post('/user', json=invalid_payload)
    response_json = response.json()

    assert response.status_code == 422
    assert (
        return_line_position(response_json.get('id', None), 'banco.txt')
        == None
    )

    # esperamos que ele não grave nada
    # esperamos o status code 422


def test_delete_with_a_valid_id():

    id = '95698a41-b3dd-4855-923c-ac561ec8ec8b'

    # encontrar o id no banco
    assert return_line_position(
        id, 'banco.txt'
    )   # asseguramos que isto está no banco

    # deletar essa linha que está o id
    response = teste.delete(f'/user/{id}')   # deletamos a linha disso no banco

    # assegurar que essa linha não existe mais
    assert return_line_position(id, 'banco.txt') == None

    # retornar status_code 200

    assert response.status_code == 200

    # exibir uma mensagem confirmando que foi deletado

    assert response.json() == {'Message': 'User Deleted'}


def test_delete_with_a_invalid_id():

    id = 'minhapica'

    # assegurar que ele não está no banco!
    assert return_line_position(id, 'banco.txt') == None

    response = teste.delete(f'/user/{id}')

    # status code == 404
    assert response.status_code == 404

    # mensagem = not found
    assert response.json() == {'Message': 'Not found'}
