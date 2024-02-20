from models import Games
from gamelib import app, db
from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from config import UPLOAD_PATH
from helpers import recover_image, delete_file, GameForm, LoginForm
import time

@app.route('/home')
def sign_in():
    games = Games.query.order_by(Games.id)
    return render_template('list.html', title='Games', games=games)


@app.route('/new')
def new():
    if 'user_logged_in' not in session or session['user_logged_in'] is None:
        return redirect(url_for('home'))
    form = GameForm()
    return render_template('form.html', title='New Game', form=form)

@app.route('/create', methods=['POST'])
def create_game():
    form = GameForm(request.form)
    if not form.validate_on_submit():
        return redirect(url_for('new'))
    
    name = form.name.data
    category = form.category.data
    console = form.console.data
    
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
        # return redirect(url_for('home'))
        return render_template('signin.html', next=next)
    game = Games.query.get(id)
    form = GameForm()
    form.name.data = game.name
    form.category.data = game.category
    form.console.data = game.console
    cover_game = recover_image(id)
    return render_template('edit.html', title='Editing Game', id=id, cover_game=cover_game, form=form)

@app.route('/update', methods=['POST'])
def update_game():
    form = GameForm(request.form)

    if form.validate_on_submit():
        game = Games.query.filter_by(id=request.form['id']).first()
        game.name = form.name.data
        game.category = form.category.data
        game.console = form.console.data

        file = request.files['file']
        timestamp = time.time()
        delete_file(game.id)
        file.save(f'{UPLOAD_PATH}/cover{game.id}-{timestamp}.jpg')

        db.session.add(game)
        db.session.commit()

    games = Games.query.order_by(Games.id)
    return render_template('list.html', title='Games', games=games)
    
@app.route("/delete/<int:id>")
def delete(id):
    if 'user_logged_in' not in session or session['user_logged_in'] is None:
        return redirect(url_for('home'))

    Games.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Game has been deleted successfully')
    return redirect(url_for('index'))

@app.route("/uploads/<filename>")
def image(filename):
    return send_from_directory('uploads', filename)