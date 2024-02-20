from gamelib import app
from flask import render_template, request, redirect, session, flash, url_for
from models import Users
from helpers import LoginForm
from flask_bcrypt import check_password_hash

@app.route('/')
def index():
    next = request.args.get('next')
    form = LoginForm()
    return render_template('signin.html', next=next, form=form)

@app.route('/authentication', methods=['POST'])
def authentication():
    form = LoginForm(request.form)
    user = Users.query.filter_by(nickname=form.username.data).first()
    password = check_password_hash(user.password, form.password.data)
    if user and password:
        session['user_logged_in'] = user.name
        flash(f"User has been logged in successfully")
        return redirect("home")
    else:
        flash(f"Not authenticated")
        return redirect(url_for('signin'))

@app.route('/logout')
def logout():
    session['user_logged_in'] = None
    flash('Logout has been done successfully')
    return redirect(url_for("index"))
