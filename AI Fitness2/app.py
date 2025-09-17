from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fitnesscare.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# User table for signup/login and personal info
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    contact = db.Column(db.String(10), unique=True, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    height = db.Column(db.Float, nullable=True)
    weight = db.Column(db.Float, nullable=True)

# Diet plan table (linked to user)
class DietPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text, nullable=False)
    calories = db.Column(db.Integer, nullable=True)
    # Add more fields as needed

# Injury record table (linked to user)
class InjuryRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    injury_type = db.Column(db.String(120), nullable=False)
    recovery_advice = db.Column(db.Text, nullable=False)
    date_reported = db.Column(db.DateTime, nullable=False)

@app.before_request
def create_tables():
    db.create_all()

users_db = {}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        age = request.form['age']
        contact = request.form['contact']
        gender = request.form['gender']
        address = request.form['address']

        import re
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_regex, email):
            error = "Invalid email format."
        elif len(contact) != 10 or not contact.isdigit():
            error = "Contact number must be exactly 10 digits."
        else:
            for u in users_db.values():
                if u['username'] == username:
                    error = "The username already exist."
                    break
                if u['email'] == email:
                    error = "Email is already existing."
                    break
                if u['contact'] == contact:
                    error = "Contact number is already existing."
                    break

        if not error:
            users_db[email] = {
                'username': username,
                'email': email,
                'password': password,
                'age': age,
                'contact': contact,
                'gender': gender,
                'address': address,
                'height': None,
                'weight': None
            }
            session['user_email'] = email
            return redirect(url_for('dashboard'))
    return render_template('signup.html', error=error)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = users_db.get(email)
        if not user:
            error = "Email not found. Please sign up."
        elif user['password'] != password:
            error = "Incorrect password."
        else:
            session['user_email'] = email
            return redirect(url_for('dashboard'))
    return render_template('login.html', error=error)

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    email = session.get('user_email')
    if not email or email not in users_db:
        return redirect(url_for('login'))

    user = users_db[email]
    info_needed = not (user.get('height') and user.get('weight') and user.get('age'))

    if request.method == 'POST':
        user['height'] = request.form.get('height')
        user['weight'] = request.form.get('weight')
        user['age'] = request.form.get('age')
        info_needed = not (user.get('height') and user.get('weight') and user.get('age'))

    return render_template(
        'dashboard.html',
        username=user['username'],
        info_needed=info_needed,
        height=user.get('height', ''),
        weight=user.get('weight', ''),
        age=user.get('age', '')
    )

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

# Placeholder routes for diet and injury
@app.route('/diet')
def diet():
    return "<h2>Your Diet Plan will appear here.</h2>"

@app.route('/injury')
def injury():
    return "<h2>Your Injury Recovery guidance will appear here.</h2>"

if __name__ == '__main__':
    app.run(debug=True)