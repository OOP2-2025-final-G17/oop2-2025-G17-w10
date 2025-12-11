from peewee import Model, CharField, DateField, IntegerField, ForeignKeyField
from .db import db
from .time import Time
from .user import User
from .product import Product


class Shift(Model):
    user = ForeignKeyField(User, backref="shifts")
    product = ForeignKeyField(Product, backref="shifts")
    date = DateField()
    time = ForeignKeyField(Time, backref="shifts")

    class Meta:
        database = db
