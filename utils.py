import bcrypt

def hashpw(user):
    if user.password:
        user.password = bcrypt.hashpw(user.password
                                                .get_secret_value()
                                                .encode('utf-8')
                                                , bcrypt.gensalt())
    return user


def checkpass(user: dict, hashed) -> bool:
    return bcrypt.checkpw(user['password'].encode("utf-8"), hashed.encode('utf-8'))