import datetime

from peewee import *

db = SqliteDatabase('comment.db')
db.connect()


class Song(Model):
    song_id = IntegerField(unique=True)
    name = CharField(max_length=360)
    comment_thread_id = CharField(max_length=360)
    create_time = DateTimeField(default=datetime.datetime.now())

    def save_(self):
        try:
            self.save()
        except IntegrityError as e:
            if 'UNIQUE' not in str(e):
                raise e

    class Meta:
        database = db


class Comment(Model):
    song_id = IntegerField()
    comment_id = IntegerField(unique=True)
    content = CharField(max_length=1000)
    like_count = IntegerField()

    class Meta:
        database = db

    def save_(self):
        try:
            self.save()
        except IntegrityError as e:
            if 'UNIQUE' not in str(e):
                raise e


db.create_tables([Song, Comment])
