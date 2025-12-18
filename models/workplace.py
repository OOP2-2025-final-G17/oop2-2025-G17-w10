from peewee import Model, CharField, DecimalField
from .db import db


class workplace(Model):
    name = CharField()
    price = DecimalField()

    class Meta:
        database = db
