from .user import user_bp
from .workplace import workplace_bp
from .order import order_bp
from .shift import shift_bp
from .time import time_bp

# Blueprintをリストとしてまとめる
blueprints = [user_bp, workplace_bp, order_bp, time_bp, shift_bp]
