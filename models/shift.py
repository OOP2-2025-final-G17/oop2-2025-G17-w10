from peewee import Model, CharField, DateField, IntegerField, ForeignKeyField
from .db import db
from .time import Time
from .user import User
from .workplace import workplace


class Shift(Model):
    user = ForeignKeyField(User, backref="shifts")
    workplace = ForeignKeyField(workplace, backref="shifts")
    date = DateField()
    time = ForeignKeyField(Time, backref="shifts")

    class Meta:
        database = db
