from mentoriaric.database.database import Users


def create(user: dict[str, str | int]) -> int:

    user['password'] = user['password'].get_secret_value()
    query = Users.insert(**user)
    _id = query.execute()
    return _id


def read(id: int):
    return Users.get_by_id(id)


def update(id: int, user_modify: dict[str, str | int]):
    return Users.update_by_id(id, user_modify)


def delete(id: int):
    return Users.delete_by_id(id)
