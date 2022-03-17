from peewee import *
from pyparsing import Char

db = SqliteDatabase('users.db')

class Users(Model):
    login = CharField(max_length=40)
    password = CharField()
    nickname = CharField(max_length=50)

    class Meta():
        database = db 

db.connect
db.create_tables([Users])

novousuario = Users(login='Rafaelbrabissimo', password='Lillia', nickname='Soleni')
novousuario.save()
