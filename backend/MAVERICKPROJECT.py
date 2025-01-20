# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 15:56:39 2025

@author: HP
"""
# Online Academic and Mentorship System Design

## Assumptions and Overview
# This system will be designed as a web application with a mobile-friendly interface.
# It will have three primary user roles: Students, Mentors, and Administrators.
# The architecture will follow a microservices pattern for scalability and modularity.
# Key technologies include Python (Django/Flask for backend), React.js for frontend, PostgreSQL for the database, and AWS for cloud hosting.

# Import Required Libraries
# Backend Framework
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token
from flask_cors import CORS

# Initialize Flask App
app = Flask(__name__)
# Enable CORS for all routes
CORS(app)  # Allow requests from all domains by default
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Best123*boy@localhost/mentorship_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'MaduMaverickChibuikem010402'

# Initialize Extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# Root route
@app.route('/')
def home():
    return "Welcome to the Flask app!"

# Define User Model
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # Student, Mentor, Admin

    def __repr__(self):
        return f"<User {self.username}>"

# Define Mentorship Sessions Model
class MentorshipSession(db.Model):
    __tablename__ = 'mentorship_sessions'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    mentor_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    scheduled_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='Scheduled')  # Scheduled, Completed, Cancelled

    def __repr__(self):
        return f"<MentorshipSession {self.id}>"

# Define Resources Model
class Resource(db.Model):
    __tablename__ = 'resources'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    url = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"<Resource {self.title}>"

# Define Progress Model
class Progress(db.Model):
    __tablename__ = 'progress'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    skill_name = db.Column(db.String(50), nullable=False)
    completion_percentage = db.Column(db.Float, default=0.0)

    def __repr__(self):
        return f"<Progress {self.student_id} - {self.skill_name}>"

# 2. User Authentication
# Registration Endpoint
@app.route('/register', methods=['POST'])
def register():
    try:
        # Log the incoming request data
        print(request.data)  # This will print raw data to the console
        
        # Parse the JSON from the request
        data = request.get_json()

        if not data:
            return jsonify({"error": "No JSON data received"}), 400

        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        role = data.get('role')

        # Ensure all required fields are present
        if not all([username, email, password, role]):
            return jsonify({"error": "Missing required fields"}), 400

        # Handle the registration logic here (e.g., saving to the database)
        return jsonify({"message": f"User {username} registered successfully!"}), 201

    except Exception as e:
        print(f"Error: {str(e)}")  # Log the error message
        return jsonify({"error": "Internal Server Error", "details": str(e)}), 500

# Login Endpoint
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        token = create_access_token(identity={"id": user.id, "role": user.role})
        return jsonify({"token": token}), 200
    return jsonify({"message": "Invalid credentials"}), 401

# 3. Mentorship Session Management
# Schedule a Session
@app.route('/schedule_session', methods=['POST'])
def schedule_session():
    data = request.get_json()
    new_session = MentorshipSession(
        student_id=data['student_id'],
        mentor_id=data['mentor_id'],
        scheduled_time=data['scheduled_time']
    )
    db.session.add(new_session)
    db.session.commit()
    return jsonify({"message": "Session scheduled successfully!"}), 201

# Get All Sessions for a User
@app.route('/sessions/<int:user_id>', methods=['GET'])
def get_sessions(user_id):
    role = request.args.get('role')
    if role == 'Student':
        sessions = MentorshipSession.query.filter_by(student_id=user_id).all()
    elif role == 'Mentor':
        sessions = MentorshipSession.query.filter_by(mentor_id=user_id).all()
    else:
        return jsonify({"message": "Invalid role"}), 400

    return jsonify([{
        "id": session.id,
        "scheduled_time": session.scheduled_time,
        "status": session.status
    } for session in sessions]), 200

# 4. Resource Management
# Add a New Resource
@app.route('/add_resource', methods=['POST'])
def add_resource():
    data = request.get_json()
    new_resource = Resource(
        title=data['title'],
        description=data['description'],
        url=data['url']
    )
    db.session.add(new_resource)
    db.session.commit()
    return jsonify({"message": "Resource added successfully!"}), 201

# Fetch All Resources
@app.route('/resources', methods=['GET'])
def get_resources():
    resources = Resource.query.all()
    return jsonify([{
        "title": resource.title,
        "description": resource.description,
        "url": resource.url
    } for resource in resources]), 200

# 5. Progress Tracking
# Update Progress
@app.route('/update_progress', methods=['POST'])
def update_progress():
    data = request.get_json()
    progress = Progress.query.filter_by(student_id=data['student_id'], skill_name=data['skill_name']).first()
    if progress:
        progress.completion_percentage = data['completion_percentage']
    else:
        progress = Progress(
            student_id=data['student_id'],
            skill_name=data['skill_name'],
            completion_percentage=data['completion_percentage']
        )
        db.session.add(progress)
    db.session.commit()
    return jsonify({"message": "Progress updated successfully!"}), 200

# Run App
#if __name__ == '__main__':
    #db.create_all()  # Make sure the database is created
    #app.run(debug=True)

if __name__ == '__main__':
    with app.app_context():  # Create the app context
        db.create_all()  # Make sure the database is created
    app.run(debug=True)