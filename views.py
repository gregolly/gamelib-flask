from models import Users, Games
from gamelib import app, db
from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from config import UPLOAD_PATH
from helpers import recover_image, delete_file
import time

@app.route('/')
def index():
    return render_template('signin.html', )

@app.route('/login')
def sign_in():
    games = Games.query.order_by(Games.id)
    return render_template('list.html', title='Games', games=games)

@app.route('/authentication', methods=['POST'])
def authentication():
    user = Users.query.filter_by(nickname=request.form['username']).first()
    if user:
        if request.form['password'] == user.password:
            session['user_logged_in'] = user.name
            flash(f"User has been logged in successfully")
            return redirect("index")
    if '123' == request.form['password']:
        username = session['user_logged_in'] = request.form['username']
        flash(f"User {username} has been logged in successfully")
        return redirect('login')
    else:
        flash(f"Not authenticated")
        return redirect(url_for('signin'))

@app.route('/logout')
def logout():
    session['user_logged_in'] = None
    flash('Logout has been done successfully')
    return redirect(url_for("index"))

@app.route('/new')
def new():
    if 'user_logged_in' not in session or session['user_logged_in'] is None:
        return redirect(url_for('login'))
    return render_template('form.html', title='New Game')

@app.route('/create', methods=['POST'])
def create_game():
    name = request.form['name']
    category = request.form['category']
    console = request.form['console']
    
    game = Games.query.filter_by(name=name).first()

    if game:
        flash('Game already exists!')
        return redirect(url_for('index'))

    new_game = Games(name=name, category=category, console=console)
    db.session.add(new_game)
    db.session.commit()

    file = request.files['file']
    timestamp = time.time()
    file.save(f'{UPLOAD_PATH}/cover{new_game.id}-{timestamp}.jpg')

    flash('Game created successfully!')
    return redirect(url_for('index'))

@app.route('/edit/<int:id>')
def edit(id):
    if 'user_logged_in' not in session or session['user_logged_in'] is None:
        # return redirect(url_for('login'))
        return render_template('signin.html', next=next)
    game = Games.query.get(id)
    cover_game = recover_image(id)
    return render_template('edit.html', title='Editing Game', game=game, cover_game=cover_game)

@app.route('/update', methods=['POST'])
def update_game():
    game = Games.query.filter_by(id=request.form['id']).first()
    game.name = request.form['name']
    game.category = request.form['category']
    game.console = request.form['console']

    file = request.files['file']
    timestamp = time.time()
    delete_file(game.id)
    file.save(f'{UPLOAD_PATH}/cover{game.id}-{timestamp}.jpg')

    db.session.add(game)
    db.session.commit()

    return redirect(url_for('index'))
    
@app.route("/delete/<int:id>")
def delete(id):
    if 'user_logged_in' not in session or session['user_logged_in'] is None:
        return redirect(url_for('login'))

    Games.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Game has been deleted successfully')
    return redirect(url_for('index'))

@app.route("/uploads/<filename>")
def image(filename):
    return send_from_directory('uploads', filename)