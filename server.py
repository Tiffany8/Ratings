"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")

@app.route('/register')
def registration():
    """Registration form for new users"""

    return render_template("register.html")

@app.route('/register', methods=["POST"])
def register_new_user():
    """Registration form for new users to GET and then POST"""
    input_email = request.form.get('email')
    input_password = request.form.get('password')
    input_age = request.form.get('age')
    input_zipcode = request.form.get('zipcode')

    new_user = User(email=input_email, password=input_password, age=input_age, zipcode=input_zipcode)

    db.session.add(new_user)
    db.session.commit()

    return redirect("/")

@app.route('/users')
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template("user_list.html", users=users)

@app.route('/movies')
def movie_list():
    """Show a list of the movies """

    movies_list = Movie.query.all()
    # rating = Rating.query.first()
    # rating.movie.title
    # would be nice to alphabetize movies
    return render_template("movie_list.html", movies_list = movies_list)

@app.route("/movies/<int:id>")
def get_movie_id(id):
    movie_object = Movie.query.get(id)
    user_id = session["logged_in_user_id"]
    # score = request.form.get("")

    # new_rating = Rating(movie_id=movie_object.movie_id, user_id=user_id, score=score)    

    # rating = Rating.query.filter_by(movie.movie_id=Rating.movie_id, 
                                    # user_id=Rating.user_id)

    # ratings_by_user = Rating.query.filter_by(user_id=user_idcode) 
  
    # Class.query.filter_by().first() # this pulls out an instance of a class

    return render_template("movie.html", movie_object=movie_object, user_id=user_id)


@app.route("/users/<int:id>")
def get_user_by_id(id):
    user = User.query.get(id)

    return render_template("user.html", user=user)



@app.route("/login")
def show_login():
    """Show login form."""

    return render_template("login.html")



@app.route("/login", methods=["POST"])
def process_login():
    """Log user into site.
    Find the user's login credentials located in the 'request.form'
    dictionary, look up the user, and store them in the session.
    """

    input_email = request.form.get('email')
    input_password = request.form.get('password')

    userq = User.query # create query object on User class

    user = userq.filter_by(email=input_email).first() # pull instance of this particular user from User class

    if user: # if there is a returned value for this user
        
        if input_password == user.password:
            session['logged_in_user_id'] = user.user_id
            # session.setdefault("logged_in_user_id", []).append(user.user_id)

            flash('Login successful')
            return redirect('/')

        else:
            flash('Incorrect password')
            return redirect('/login')

    else: 
        flash('No such email')
        return redirect('/login')

@app.route("/logout")
def logout():
    """Logout user"""
    del session['logged_in_user_id']
    flash("You have been logged out.")
    return redirect('/')
    




if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()


