from peewee import Model, CharField, DateField, IntegerField, ForeignKeyField
from .db import db
from .time import Time
from .user import User
from .workplace import Workplace


class Shift(Model):
    user = ForeignKeyField(User, backref="shifts")
    workplace = ForeignKeyField(Workplace, backref="shifts")
    date = DateField()
    time = ForeignKeyField(Time, backref="shifts")

    class Meta:
        database = db
