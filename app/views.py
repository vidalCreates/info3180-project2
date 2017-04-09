"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

import os
from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
from forms import LoginForm
from forms import RegisterForm
from forms import NewItemForm
from models import UserProfile, WishlistItem

import uuid
import re
from image_getter import getimageurls

###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html', form=None)


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')


@app.route("/api/users/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "POST":

        if form.validate_on_submit():
            # get data from form
            email = form.email.data
            password = form.password.data

            # retrieve user from database
            user = UserProfile.query.filter_by(email=email, password=password).first()

            if user is not None:
                # login user
                login_user(user)

                # flash user for successful login
                flash('Logged in as '+current_user.first_name+" "+current_user.last_name, 'success')

                # redirect user to their wishlist page
                return redirect(url_for("wishlist", userid=current_user.get_id()))

            # flash user for failed login
            flash('Your email or password is incorrect', 'danger')
            return redirect(url_for("login")) #
        else:
            # flash user for incomplete form
            flash('Invalid login data, please try again', 'danger')
    return render_template("login.html", form=form)


@app.route("/api/users/logout")
@login_required
def logout():
    logout_user()
    flash('Logged out.', 'danger')
    return redirect(url_for("login"))


@app.route("/api/users/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if request.method == "POST":
        if form.validate_on_submit():
            # generate userid
            userid = str(uuid.uuid4().fields[-1])[:8]

            # get data from form
            firstname = form.firstname.data
            lastname = form.lastname.data
            email = form.email.data
            password = form.password.data

            # retrieve user from database
            user = UserProfile.query.filter_by(email=email, password=password).first()

            # if the user already exists then flash error message and redirect back to the registration page
            if user is not None:
                flash('An account with that email address already exists', 'danger')
                return redirect(url_for('register'))

            # create user object
            user = UserProfile(id=userid,
                               first_name=firstname,
                               last_name=lastname,
                               email=email,
                               password=password)

            # insert user into UserProfile
            db.session.add(user)
            db.session.commit()
            # quit()

            # logout old user
            logout_user()

            # login new user
            login_user(user)

            # flash the user for successful registration
            flash('Registration Successful, Welcome '+current_user.first_name, 'success')

            # redirect user to their wishlist page
            return redirect(url_for("wishlist", userid=current_user.get_id()))

        else:
            flash('Please fill in all fields', 'danger')
            return redirect(url_for('register'))

    return render_template("register.html", form=form)


@app.route("/api/users/<int:userid>/wishlist", methods=["GET", "POST"])
@login_required
def wishlist(userid):
    # file_folder = app.config['UPLOAD_FOLDER']
    form = NewItemForm()
    if request.method == "POST":
        if form.validate_on_submit():
            # generate item id
            id = str(uuid.uuid4().fields[-1])[:8]

            # get data from form
            title = form.title.data
            description = form.description.data
            webaddress = form.webaddress.data
            thumbnail = request.form['thumbnail']

            # retrieve item from database
            item = WishlistItem.query.filter_by(title=title, owner=current_user.get_id()).first()

            # if the item already exists then flash error message and redirect back to the wishlist page
            if item is not None:
                flash(''+title+' already exists in your wishlist', 'danger')
                return redirect(url_for('wishlist', userid=current_user.get_id()))

            # create wishlist object
            item = WishlistItem(id=id,
                                owner=current_user.get_id(),
                                title=title,
                                description=description,
                                webaddress=webaddress,
                                thumbnail=thumbnail)

            # insert item into WishlistItem
            db.session.add(item)
            db.session.commit()

            # redirect user to their wishlist page
            return redirect(url_for("wishlist", userid=current_user.get_id()))
        else:
            # flash message for failed item addition
            flash('Invalid item data, please try again', 'danger')

            # redirect user to their wishlist page
            return redirect(url_for("wishlist", userid=current_user.get_id()))
    else:
        # retrieve user from database
        items = WishlistItem.query.filter_by(owner=current_user.get_id()).all()
    return render_template("wishlist.html", userid=current_user.get_id(), form=form, items=items)


@app.route("/api/users/<int:userid>/wishlist/<int:itemid>", methods=["GET", "DELETE"])
@login_required
def removeitem(userid, itemid):
    if request.method == "DELETE":
        # flash user for successful delete
        flash('Item deleted', 'success')

        # remove item from wishlist
        db.session.delete(WishlistItem.query.filter_by(id=itemid).first())
        db.session.commit()

        # redirect user to their wishlist page
        return redirect(url_for("wishlist", userid=current_user.get_id()))
    else:
        # flash user for successful delete
        flash('Item deleted', 'success')

        # remove item from wishlist
        db.session.delete(WishlistItem.query.filter_by(id=itemid).first())
        db.session.commit()

        return redirect(url_for("wishlist", userid=current_user.get_id()))

# user_loader callback. This callback is used to reload the user object from
# the user ID stored in the session


@app.route('/api/thumbnails', methods=['GET'])
def thumbnails():
    # get url from form
    url = request.args.get('url')

    # establish regular expression for url
    pattern = re.compile("(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9]\.[^\s]{2,})")

    # if the text entered is a url then scrape for images
    if pattern.match(url):
        # get and return thumbnails
        return jsonify({'error': None, 'message': 'Success', 'thumbnails': getimageurls(url)})

    # otherwise display default image
    return jsonify({'error': None, 'message': 'Success', 'thumbnails': [url_for('static', filename="uploads/placeholder.png")]})


@login_manager.user_loader
def load_user(id):
    return UserProfile.query.get(int(id))


@login_manager.unauthorized_handler
def unauthorized_handler():
    flash('Restricted access. Please login to access this page.', 'danger')
    return redirect(url_for('login'))
###
# The functions below should be applicable to all Flask apps.
###


@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")
