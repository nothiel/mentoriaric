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


db.connect()

db.create_tables([Users])

