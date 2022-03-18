from database import Users
from utils import checkpass, hashpw

def create(user: dict[str, str|int]) -> int | None:
    return Users.create_user(user)

def read(id: int) -> dict[str, str|int] | None:
    return Users.get_by_id(id)

def update(sets, id: int) -> int | None:
    sets = sets.dict(exclude_unset=True)
    if 'password' in sets:
        sets['password'] = hashpw(sets)
    return Users.update_by_id(sets, id)

def delete(id: int) -> int | None:
    return Users.delete_user_by_id(id)

def checkapass(user) -> bool:
    hashed = Users.get_password(user['login'])
    if hashed:
        return checkpass(user, hashed)
    
    