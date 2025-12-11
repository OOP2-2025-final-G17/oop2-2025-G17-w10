from peewee import Model, CharField, DateField, IntegerField
from .db import db


class Shift(Model):
    name = CharField()
    workplace = IntegerField()
    date = DateField()

    class Meta:
        database = db
