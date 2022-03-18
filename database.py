from peewee import *

db = SqliteDatabase('users.db')



class Users(Model): # create table users (
    login = CharField(max_length=50) # login varchar(50),
    password = CharField() # password varchar(255),
    nickname = CharField(max_length=50) # nickname varchar(50) )

    @classmethod
    def get_as_dict(cls, where):
        try: 
            query = cls.select().where(where).dicts()
            return query.get()
        except DoesNotExist:
            return None
    class Meta:
        database = db # use users

    @classmethod
    def get_by_id(cls, id: int) -> dict[str, str|int] | None:
        try:
            query = cls.select(Users.id, Users.login, Users.nickname).where(Users.id == id).dicts()
            return query.get()
        except DoesNotExist:
            return None

    @classmethod
    def update_by_id(cls, sets: dict, id: int) -> int | None:
        try:
            query = cls.update(**sets).where(Users.id == id)
            return query.execute()
        except Exception as err:
            print(f"ERROR WHILE UPDATING DATABASE: {err}")
            return None

    
    @classmethod
    def create_user(cls, insert_data: dict[str, str|int]) -> int | None:
        try:
            query = cls.insert(**insert_data).execute()
            return query
        except Exception as err:
            print(f"ERROR WHILE INSERTING ON DATABASE: {err}")
            return None

    @classmethod
    def delete_user_by_id(cls, id: int) -> int | None:
        try:
            return cls.delete().where(Users.id == id).execute()
        except Exception as err:
            print(f"ERROR WHILE DELETING ROW: {err}")
            return None

    @classmethod
    def get_password(cls, login):
        try:
            [password] = cls.select(Users.password).where(Users.login == login).dicts().get().values()
            return password
        except DoesNotExist:
            return None


db.connect()

db.create_tables([Users])

