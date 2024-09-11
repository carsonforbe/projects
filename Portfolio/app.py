from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a secure key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Define User model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    tasks = db.relationship('Task', backref='author', lazy=True)

# Define Task model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    due_date = db.Column(db.String(50), nullable=False)
    priority = db.Column(db.String(50), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
@login_required
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('home'))
        return "Invalid credentials", 401
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if User.query.filter_by(username=username).first():
            return "Username already exists", 400
        hashed_password = generate_password_hash(password, method='sha256')
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/add_task', methods=['POST'])
@login_required
def add_task():
    task_data = request.json
    task = Task(
        text=task_data.get('text'),
        due_date=task_data.get('due_date'),
        priority=task_data.get('priority'),
        user_id=current_user.id
    )
    db.session.add(task)
    db.session.commit()
    return jsonify({
        'id': task.id,
        'text': task.text,
        'due_date': task.due_date,
        'priority': task.priority,
        'completed': task.completed
    }), 201

@app.route('/get_tasks', methods=['GET'])
@login_required
def get_tasks():
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    task_list = [{
        'id': task.id,
        'text': task.text,
        'due_date': task.due_date,
        'priority': task.priority,
        'completed': task.completed
    } for task in tasks]
    return jsonify(task_list)

@app.route('/delete_task', methods=['POST'])
@login_required
def delete_task():
    task_id = request.json.get('id')
    task = Task.query.get_or_404(task_id)
    if task.user_id == current_user.id:
        db.session.delete(task)
        db.session.commit()
        return jsonify({'message': 'Task deleted'}), 200
    return jsonify({'message': 'Unauthorized'}), 403

@app.route('/complete_task', methods=['POST'])
@login_required
def complete_task():
    task_id = request.json.get('id')
    task = Task.query.get_or_404(task_id)
    if task.user_id == current_user.id:
        task.completed = not task.completed
        db.session.commit()
        return jsonify({'message': 'Task marked as completed' if task.completed else 'Task marked as pending'}), 200
    return jsonify({'message': 'Unauthorized'}), 403

@app.cli.command('create_db')
def create_db():
    """Create database tables."""
    with app.app_context():
        db.create_all()
    print('Database tables created.')

if __name__ == '__main__':
    if not os.path.exists('site.db'):
        print("Database not found. Run 'flask create_db' to create it.")
    app.run(debug=True)
