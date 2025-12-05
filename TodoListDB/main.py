from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SECRET_KEY'] = 'your_secret_key_here'

db = SQLAlchemy(app)


# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    todos = db.relationship('Todo', backref='user', lazy=True, cascade='all, delete-orphan')


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


# Routes
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect('/dashboard')
    return redirect('/login')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            return render_template('signup.html', error='Username and password required')

        if User.query.filter_by(username=username).first():
            return render_template('signup.html', error='Username already exists')

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect('/login')

    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if not user or not check_password_hash(user.password, password):
            return render_template('login.html', error='Invalid username or password')

        session['user_id'] = user.id
        session['username'] = user.username
        return redirect('/dashboard')

    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')

    user = User.query.get(session['user_id'])
    todos = Todo.query.filter_by(user_id=session['user_id']).all()

    return render_template('dashboard.html', username=user.username, todos=todos)


@app.route('/add_todo', methods=['POST'])
def add_todo():
    if 'user_id' not in session:
        return redirect('/login')

    title = request.form.get('title').strip()

    if not title:
        return redirect('/dashboard')

    new_todo = Todo(title=title, user_id=session['user_id'])
    db.session.add(new_todo)
    db.session.commit()

    return redirect('/dashboard')


@app.route('/complete_todo/<int:todo_id>', methods=['POST'])
def complete_todo(todo_id):
    if 'user_id' not in session:
        return redirect('/login')

    todo = Todo.query.get(todo_id)

    if todo and todo.user_id == session['user_id']:
        todo.completed = not todo.completed
        db.session.commit()

    return redirect('/dashboard')


@app.route('/delete_todo/<int:todo_id>', methods=['POST'])
def delete_todo(todo_id):
    if 'user_id' not in session:
        return redirect('/login')

    todo = Todo.query.get(todo_id)

    if todo and todo.user_id == session['user_id']:
        db.session.delete(todo)
        db.session.commit()

    return redirect('/dashboard')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)