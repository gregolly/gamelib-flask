from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'your secret key'

app.config['SQLALCHEMY_DATABASE_URI'] = \
'{SGBD}://{user}:{password}@{server}/{database}'.format(
    SGBD = 'mysql+mysqlconnector',
    user = 'root',
    password = 'admin',
    server = 'localhost',
    database = 'jogoteca'
)

db = SQLAlchemy(app)

class Jogos(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50), nullable=False)
    categoria = db.Column(db.String(40), nullable=False)
    console = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name
    
class Usuarios(db.Model):
    nome = db.Column(db.String(20), nullable=False)
    nickname = db.Column(db.String(8), nullable=False, primary_key=True)
    senha = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name

@app.route('/')
def index():
    games = Jogos.query.order_by(Jogos.id)
    return render_template('list.html', title='Games', games=games)

@app.route('/new')
def new():
    if 'user_logged_in' not in session or session['user_logged_in'] == None:
        return redirect(url_for('login', value=url_for('new')))
    return render_template('form.html', title='New Game')

@app.route('/create', methods=['POST'])
def create_game():
    name = request.form['name']
    category = request.form['category']
    console = request.form['console']
    
    jogo = Jogos.query.filter_by(nome=name).first()

    if jogo:
        flash('Game has exist already!')
        return redirect(url_for('index'))

    new_game = Jogos(nome=name, categoria=category, console=console)
    db.session.add(new_game)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/login')
def sign_in():
    next = request.args.get('next')
    return render_template('signin.html', next=next)

@app.route('/authentication', methods=['POST'])
def authentication():
    user = Usuarios.query.filter_by(nickname=request.form['username']).first()
    if user:
        if request.form['password'] == user.senha:
            session['user_logged_in'] = user.nome
            flash(f"User has been logged in successfully")
            next_page = request.form['next']
            return redirect(next_page)
    if '123' == request.form['password']:
        username = session['user_logged_in'] = request.form['username']
        flash(f"User {username} has been logged in successfully")
        next_page = request.form['next']
        return redirect(next_page)
    else:
        flash(f"Not authenticated")
        return redirect(url_for('signin'))

@app.route('/logout')
def logout():
    session['user_logged_in'] = None
    flash('Logout has been done successfully')
    return redirect(url_for("index"))

app.run(debug=True)