from flask import Flask, render_template, request, redirect, session, flash, url_for

class Game:
    def __init__(self, name, category, console) -> None:
        self.name = name
        self.category = category
        self.console = console

class User:
    def __init__(self, username, password) -> None:
        self.username = username
        self.password = password

games = []

user_one = User('guilherme', '123')
user_two = User('larissa', '1234')
user_three = User('michele', '12345')

users = {
    user_one.username: user_one,
    user_two.username: user_two,
    user_three.username: user_three
}

app = Flask(__name__)
app.secret_key = 'your secret key'

@app.route('/index')
def index():
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
    game = Game(name, category, console)
    games.append(game)

    return redirect(url_for('index'))

@app.route('/signin')
def sign_in():
    next = request.args.get('next')
    return render_template('signin.html', next=next)

@app.route('/authentication', methods=['POST'])
def authentication():
    if request.form['username'] in users:
        user = users[request.form['username']]
        if request.form['password'] == user.password:
            session['user_logged_in'] = user.username
            flash(f"User {user.username} has been logged in successfully")
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