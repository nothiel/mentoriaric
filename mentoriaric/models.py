from pydantic import BaseModel, SecretStr


class User(BaseModel):
    login: str
    password: SecretStr
    nickname: str


class UserModify(BaseModel):
    login: str | None
    password: str | None
    nickname: str | None
