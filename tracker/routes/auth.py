from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash

from tracker.extensions import db
from tracker.models import User

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if not user or not check_password_hash(user.password, password):
            flash('The username or password entered is incorrect!', 'error')
            return redirect(url_for('auth.login'))
            
        else:
            login_user(user)
            return redirect(url_for('main.index'))

    return render_template('login.html')


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        unhashed_password = request.form['password']
        user_type = request.form['user_type']

        user = User(
            username=username,
            unhashed_password=unhashed_password,
            admin = True if int(user_type) == 1 else False,
            user_type=int(user_type))

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('auth.login'))

    return render_template('register.html')


@auth.route("/logout")
def logout():
    logout_user()
    flash('You have successfully been logged out', 'success')
    return redirect(url_for('main.index'))
