import hashlib

import datetime
from peewee import *

from local_settings import USER_DATABASE
from local_settings import PASSWORD_DATABASE



database = MySQLDatabase('fastapi_project', 
        user=USER_DATABASE,
        password=PASSWORD_DATABASE,
        host='localhost',
        port=3306)


class User(Model):
    username = CharField(max_length=50, unique=True)
    password = CharField(max_length=50)
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = database
        table_name = 'users'


    @classmethod
    def create_password(cls, password):
        h = hashlib.md5()
        h.update(password.encode('utf-8'))

        return h.hexdigest()


    @classmethod
    def authenticate(cls, username, password):
        user = cls.select().where(User.username == username).first()
#ps aux | grep mysql
        if user and user.password == User.create_password(password):
            return user


    def __str__(self):
        return self.username


class Movie(Model):
    title = CharField(max_length=50)
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = database
        table_name = 'movies'


class UserReview(Model):
    user = ForeignKeyField(User, backref='reviews')
    movie = ForeignKeyField(Movie)
    review = TextField()
    score = IntegerField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = database
        table_name = 'user_reviews'

    def __str__(self):
        return f'{self.user.username} - #{self.movie.title}'
