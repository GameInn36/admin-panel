import base64
from datetime import datetime
import json
from flask import current_app, render_template, request, redirect, url_for, flash, abort
from flask_login.utils import login_required
from passlib.hash import pbkdf2_sha256 as hasher
from user import get_user, User
from forms import LoginForm, SignupForm
from flask_login import login_user, logout_user, current_user
import os
import re



@login_required
def home_page():
    p = current_app.config["p"]
    if request.method == "GET":
        return render_template("movies_search.html")
    else:
        title = request.form["title"]
        #score = request.form["score"]
        #lang = request.form["answer"]
        #genres = request.form.getlist("genres")

        #movies = db.search_movie(title, score, lang, genres)
        games = p.search_game(title)
        return render_template("search.html", movies=games) 
        return render_template("add_movie.html", values = {"title": "o", "year": "12", "avg_vote": "5"}) 

@login_required
def user_search():
    p = current_app.config["p"]
    if request.method == "GET":
        return render_template("user_search.html")
    else:
        title = request.form["title"]

        #movies = db.search_movie(title, score, lang, genres)
        users = p.search_user(title)
        print(users)
        return render_template("user_search_results.html", movies=users) 
        return render_template("add_movie.html", values = {"title": "o", "year": "12", "avg_vote": "5"}) 


def delete_profile_page():
    db = current_app.config["db"]
    username = current_user.username
    logout_user()
    db.delete_user(username)

    return redirect(url_for("home_page"))

@login_required
def add_game_new_page():
        p = current_app.config["p"]
        if request.method == "GET":
            values = {"title": "o", "year": "12", "avg_vote": "5"}
            return render_template(
                "add_movie.html",
                values=values,
            )
        else:
            valid = validate_movie_form_new(request.form)
            if not valid:
                return render_template(
                    "add_movie.html",
                    min_year=1887,
                    max_year=datetime.now().year,
                    values=request.form,
                    min_score = 0,
                    max_score = 10
                )

            dict_object = {}

            uploaded_file = request.files.get('cover')
            print(uploaded_file)
            extensions = ['.jpg', '.png', '.gif']
            path = 'uploads' 
            if not uploaded_file is None and uploaded_file.filename != '':
                filename = uploaded_file.filename
                file_ext = os.path.splitext(filename)[1]
                if file_ext not in extensions:
                    abort(400)



                uploaded_file.save(os.path.join(path, uploaded_file.filename))
            title = request.form.data["title"]
            print(title)
            description = request.form.data["description"]
            print(description)
            timestamp = request.form.data["timestamp"]
            print(timestamp)
            platforms = request.form.getlist("platforms")
            print(platforms)
            genres = request.form.getlist("genres")
            print(genres)
            publisher = request.form.data["publisher"]

            dict_object["name"] = title
            dict_object["summary"] = description
            dict_object["first_release_date"] = timestamp
            dict_object["publisher"] = publisher
            dict_object["genres"] = genres
            dict_object["platforms"] = platforms

            if uploaded_file is not None:
                dosyam = open(os.path.join(path, uploaded_file.filename), "rb")
                #print(dosyam)
                dict_object["cover"] = str(base64.b64encode(dosyam.read()))[2:-1]
            dict_object["logCount"] = 0

            json_object = json.dumps(dict_object, indent = 4) 
            #print(json_object)
            p.add_game(dict_object)
            with open("sample.json", "w") as outfile:
                outfile.write(json_object)
            #movie = Movie("", title, year, "", "", "", "", "", "Unknown", "", "", avg_vote, 0)
            #db = current_app.config["db"]
            #imdb_title_id = db.add_movie_new(movie)
            return redirect(url_for("home_page"))
            return render_template("movies_search.html")
            return redirect(url_for("movie_new", imdb_id = imdb_title_id))

def delete_game_page(id):
    #db = current_app.config["db"]
    #db.delete_movie_new(imdb_title_id)
    p = current_app.config["p"]
    p.delete_game(id)
    return redirect(url_for("home_page"))

def delete_user_page(id):
    #db = current_app.config["db"]
    #db.delete_movie_new(imdb_title_id)
    p = current_app.config["p"]
    p.delete_user(id)
    return redirect(url_for("home_page"))

def validate_movie_form_new(form):
    form.data = {}
    form.errors = {}

    form_title = form.get("title", "").strip()
    form_description = form.get("description", "").strip()
    form_publisher = form.get("publisher", "").strip()
    #form_director = form.get("director", "").strip()
    if len(form_title) == 0:
        form.errors["title"] = "Title can not be blank."
    else:
        form.data["title"] = form_title

    if len(form_description) == 0:
        form.errors["description"] = "Description can not be blank."
    else:
        form.data["description"] = form_description

    if len(form_publisher) == 0:
        form.errors["publisher"] = "Publisher can not be blank."
    else:
        form.data["publisher"] = form_publisher
    

    form_avg_vote = form.get("avg_vote")
    if not form_avg_vote:
        form.data["avg_vote"] = 0
    elif (not form_avg_vote.isdigit()) and (re.match(r'^-?\d+(?:\.\d+)$', str(form_avg_vote)) is None):
        form.errors["avg_vote"] = "Average Vote must consist of digits only."
    else:
        avg_vote = float(form_avg_vote)
        if (avg_vote < 0) or (avg_vote > 10):
            form.errors["avg_vote"] = "Average vote not in valid range."
        else:
            form.data["avg_vote"] = avg_vote

    form_year = form.get("timestamp")
    year = int(form_year)
    if year >= 0 and year < 2147483647:
        form.data["timestamp"] = year
    else:
        form.errors["timestamp"] = "Timestamp must be larger than 0 and less than 2,147,483,647."
    

    return len(form.errors) == 0




def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.data["username"]
        password = form.data["password"]
        user = User(username, password)
        if user.username == "admin":
            if user.password == "admin":
                login_user(user)
                flash("You have logged in.")
                next_page = request.args.get("next", url_for("home_page"))
                return redirect(next_page)
        flash("Invalid credentials.")
    return render_template("login.html", form=form)


def logout_page():
    logout_user()
    flash("You have logged out.")
    return redirect(url_for("home_page"))







