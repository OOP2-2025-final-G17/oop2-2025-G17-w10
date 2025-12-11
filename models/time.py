from peewee import Model, CharField, TimeField
from .db import db

class Time(Model):
    name = CharField()
    start_time = TimeField(null=True)
    end_time = TimeField(null=True)
    break_start_time=TimeField(null=True)
    break_end_time=TimeField(null=True)

    class Meta:
        database = db