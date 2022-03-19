from peewee import *

db = SqliteDatabase('users.db')


class BaseModel(Model):
    class Meta:
        database = db


class Users(BaseModel):   # create table users (
    login = CharField(max_length=50)   # login varchar(50),
    password = CharField()   # password varchar(255),
    nickname = CharField(max_length=50)   # nickname varchar(50) )

    @classmethod
    def get_as_dict(cls, where):
        try:
            query = cls.select().where(where).dicts()
            return query.get()
        except DoesNotExist:
            return None

    @classmethod
    def get_by_id(cls, id):
        try:
            query = (
                cls.select(Users.id, Users.login, Users.nickname)
                .where(Users.id == id)
                .dicts()
            )
            return query.get()
        except DoesNotExist:
            return None

    @classmethod
    def update_by_id(cls, id, modify):
        try:
            query = cls.update(**modify).where(Users.id == id)
            return query.execute()
        except Exception as err:
            print(f'DEU PAU NO BANCO DE DADOS: {err}')
            return None

    @classmethod
    def delete_by_id(cls, id):
        try:
            query = cls.delete().where(Users.id == id)
            return query.execute()
        except Exception as err:
            print(f'DEU PAU NO BANCO DE DADOS: {err}')
            return None


db.connect()

db.create_tables([Users])
