from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
from flask_login import LoginManager
from werkzeug.security import generate_password_hash
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['JWT_SECRET_KEY'] = os.getenv('SECRET_KEY')
login = LoginManager(app)
login.login_view = "login"
db = SQLAlchemy(app)
jwt = JWTManager(app)

if __name__ == '__main__':
    app.run(debug=True)

from app import routes
from app.models import User, Task, TaskStatus, TaskHistory

@app.route('/api/register', methods=['POST'])
def api_register():
    data = request.get_json()
    username = data['username']
    password = data['password']
    existing_user = User.query.filter_by(username=username).first()

    if existing_user:
        return jsonify({'message': 'Username already exists'}), 401

    new_user = User(username=username, hashed_password = generate_password_hash(password))
    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User created successfully'}), 201
    except:
        return jsonify({'message': 'Username/password too long'}), 401
    
@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()

    if user and user.check_password(data['password']):
        token = create_access_token(identity=user.id)
        return jsonify(token=token), 200
    else:
        return jsonify({'message': 'Invalid credentials!'}), 401
    
@app.route('/api/get_tasks', methods=['GET'])
@jwt_required()
def api_get_tasks():
    try:
        user_id = get_jwt_identity()
        tasks = Task.query.filter_by(id=user_id).all()
        return jsonify(tasks=[task.dictionize() for task in tasks])
    except Exception as e:
        print(f"Error getting tasks for user {user_id}: {e}")
        return jsonify({'message': 'Invalid or expired token'}), 401
    
@app.route('/api/create_task', methods=['POST'])
@jwt_required()
def api_create_task():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        if 'status' in data:
            status_code = int(data['status'])
        else:
            status_code = 0

        new_task = Task(
            title=data.get('title'),
            status=TaskStatus(status_code),
            user_id=User.query.filter_by(id=user_id).first()
        )

        db.session.add(new_task)
        db.session.commit()

        return jsonify({'message': 'Task added successfully'}), 201
    except Exception as e:
        print(f"Error adding task: {e}")
        return jsonify({'message': 'Error adding task'}), 500

@app.route('/api/delete_task/<int:task_id>', methods=['DELETE'])
@jwt_required()
def api_delete_task(task_id):
    try:
        user_id = get_jwt_identity()
        user_obj = User.query.filter_by(id=user_id).first()

        task_to_delete = Task.query.filter_by(id=task_id).first()
        if not task_to_delete:
            return jsonify({'message': 'Task not found'}), 404
        
        if task_to_delete.user_id != user_obj:
            return jsonify({'message': 'Unauthorized'}), 401

        new_task_history = TaskHistory(user_id=user_id, task_id = task_id)
        db.session.add(new_task_history)

        db.session.delete(task_to_delete)

        db.session.commit()

        return jsonify({'message': 'Task deleted successfully'}), 200
    except Exception as e:
        print(f"Error deleting task: {e}")
        return jsonify({'message': 'Error deleting task'}), 500
    
@app.route('/api/update_task/<int:task_id>', methods=['PATCH'])
@jwt_required()
def api_update_task(task_id):
    try:
        user_id = get_jwt_identity()
        user_obj = User.query.filter_by(id=user_id).first()

        task_to_update = Task.query.filter_by(id=task_id).first()
        if not task_to_update:
            return jsonify({'message': 'Task not found'}), 404
        
        if task_to_update.user_id != user_obj:
            return jsonify({'message': 'Unauthorized'}), 401
        
        data = request.get_json()
        task_to_update.status = TaskStatus(int(data.get('status', task_to_update.status)))
        task_to_update.title = data.get('title', task_to_update.title)

        db.session.commit()

        return jsonify({'message': 'Task updated successfully'}), 200
    except Exception as e:
        print(f"Error updating task: {e}")
        return jsonify({'message': 'Error updating task'}), 500