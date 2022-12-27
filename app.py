from flask import Flask
from flask_login import LoginManager
from passlib.hash import pbkdf2_sha256 as hasher
import os

import views
from poster import Poster
from user import get_user

lm = LoginManager()

@lm.user_loader
def load_user(user_id):
    return get_user(user_id)


def create_app():
    app = Flask(__name__)
    app.config.from_object("settings")
      

    app.add_url_rule("/", view_func=views.home_page, methods=["GET", "POST"])
    app.add_url_rule("/user_search", view_func=views.user_search, methods=["GET", "POST"])
    app.add_url_rule("/login", view_func=views.login_page, methods=["GET", "POST"])
    app.add_url_rule("/add_game", view_func=views.add_game_new_page, methods=["GET", "POST"])
    app.add_url_rule("/delete_game/<string:id>", view_func=views.delete_game_page)
    app.add_url_rule("/delete_user/<string:id>", view_func=views.delete_user_page)
    app.add_url_rule("/delete_review", view_func=views.delete_review, methods=["GET", "POST"])
    app.add_url_rule("/logout", view_func=views.logout_page)

    lm.init_app(app)
    lm.login_view = "login_page"




    poster = Poster()
    app.config["p"] = poster

   
    return app

app = create_app()


if __name__ == "__main__":
    port = app.config.get("PORT", 5000)
    app.run(host="0.0.0.0", port=port)