from datetime import date
from flask import Flask, render_template
from models import initialize_database
from models.shift import Shift
from routes import blueprints

app = Flask(__name__)

# データベースの初期化
initialize_database()

# 各Blueprintをアプリケーションに登録
for blueprint in blueprints:
    app.register_blueprint(blueprint)


# ホームページのルート
@app.route("/")
def index():
    today_date = date.today()            

    shifts = Shift.select().where(Shift.date == today_date)

    return render_template(
        "index.html",
        today=today_date,
        today_shifts=shifts,
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
