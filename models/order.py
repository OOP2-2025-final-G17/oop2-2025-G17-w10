from peewee import Model, ForeignKeyField, DateTimeField
from .db import db
from .user import User
from .workplace import workplace


class Order(Model):
    user = ForeignKeyField(User, backref="orders")
    workplace = ForeignKeyField(workplace, backref="orders")
    order_date = DateTimeField()

    class Meta:
        database = db
