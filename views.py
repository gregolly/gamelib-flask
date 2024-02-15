from models import Users, Games
from gamelib import app, db
from flask import render_template, request, redirect, session, flash, url_for

@app.route('/')
def index():
    games = Games.query.order_by(Games.id)
    return render_template('list.html', title='Games', games=games)

@app.route('/login')
def sign_in():
    next = request.args.get('next')
    return render_template('signin.html', next=next)

@app.route('/authentication', methods=['POST'])
def authentication():
    user = Users.query.filter_by(nickname=request.form['username']).first()
    if user:
        if request.form['password'] == user.senha:
            session['user_logged_in'] = user.nome
            flash(f"User has been logged in successfully")
            return redirect("/new")
    if '123' == request.form['password']:
        username = session['user_logged_in'] = request.form['username']
        flash(f"User {username} has been logged in successfully")
        return redirect('/new')
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
    flash('Game created successfully!')
    return redirect(url_for('index'))

@app.route('/edit/<int:id>')
def edit(id):
    if 'user_logged_in' not in session or session['user_logged_in'] is None:
        return redirect(url_for('login'))
    game = Games.query.get(id)
    return render_template('edit.html', title='Editing Game', game=game)

@app.route('/update', methods=['POST'])
def update_game():
    game = Games.query.filter_by(id=request.form['id']).first()
    game.name = request.form['name']
    game.category = request.form['category']
    game.console = request.form['console']

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

