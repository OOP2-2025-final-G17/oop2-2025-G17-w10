from flask import Flask, render_template
from models import initialize_database
from routes import blueprints
from models.db import db
from models.user import User
from models.workplace import Workplace
from models.time import Time
from models.shift import Shift
from collections import OrderedDict

app = Flask(__name__)

# データベースの初期化
initialize_database()

# 各Blueprintをアプリケーションに登録
for blueprint in blueprints:
    app.register_blueprint(blueprint)


# ホームページのルート
@app.route("/")
def index():
    query = (
            Shift
            .select(Shift, Workplace, User)
            .join(Workplace)          # Shift.workplace
            .switch(Shift)
            .join(User)               # Shift.user
            .order_by(Workplace.name, User.name)
        )
    workplace_to_users = OrderedDict()

    for s in query:
            wp_name = s.workplace.name
            if wp_name not in workplace_to_users:
                workplace_to_users[wp_name] = OrderedDict()

            # 同じ職場に同じ人が複数シフトあっても 1 回だけ表示
            workplace_to_users[wp_name][s.user.id] = s.user.name
    groups = [
            {"workplace": wp_name, "users": list(users.values())}
            for wp_name, users in workplace_to_users.items()
        ]


    return render_template("index.html", groups=groups)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
