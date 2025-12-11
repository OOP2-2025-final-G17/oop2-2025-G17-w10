from peewee import SqliteDatabase
from .db import db
from .user import User
from .product import Product
from .time import Time
from .shift import Shift

# モデルのリストを定義しておくと、後でまとめて登録しやすくなります
MODELS = [
    User,
    Product,
    Time,
    Shift,
]


# データベースの初期化関数
def initialize_database():
    db.connect()
    db.create_tables(MODELS, safe=True)
    db.close()
