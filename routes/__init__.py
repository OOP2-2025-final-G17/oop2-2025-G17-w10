from .user import user_bp
from .workplace import workplace_bp
from .shift import shift_bp
from .time import time_bp
from .calendar import calendar_bp

# Blueprintをリストとしてまとめる
blueprints = [user_bp, workplace_bp, time_bp, shift_bp, calendar_bp]
