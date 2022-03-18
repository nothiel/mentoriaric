from pydantic import BaseModel, SecretStr, root_validator

class User(BaseModel):
    login: str
    password: SecretStr
    nickname: str


class UserModify(BaseModel):
    login: str | None
    password: str | None
    nickname: str | None

    @root_validator
    def any_of(cls, v):
        if not any(v.values()):
            raise ValueError('no field inserted')
        return v