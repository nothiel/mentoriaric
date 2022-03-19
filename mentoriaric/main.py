from fastapi import FastAPI
from mentoriaric.models import User, UserModify
from mentoriaric.services import create, delete, read, update
from starlette.responses import JSONResponse

app = FastAPI()


@app.get('/')
def root():
    return {'Hello': 'World!'}


@app.post('/user')
def create_user(user: User):

    _id = create(user.dict())

    return JSONResponse({'Message': f'User created', 'id': _id}, 201)


@app.get('/user/{id}')
def get_user(id: int):

    user = read(id)
    if not user:
        return JSONResponse({'Message': 'not found'}, 404)

    return JSONResponse({'User': user}, 200)


@app.put('/user/{id}')
def modify_user(id: int, modify_user: UserModify):

    is_modified = bool(update(id, modify_user.dict(exclude_unset=True)))

    if not is_modified:
        return JSONResponse({'Message': 'Not found'}, 404)

    return JSONResponse({'Message': 'User modified'}, 200)


@app.delete('/user/{id}')
def delete_user(id):

    is_deleted = bool(delete(id))

    if not is_deleted:
        return JSONResponse({'Message': 'Not found'}, 404)

    return JSONResponse({'Message': 'User Deleted'}, 200)
