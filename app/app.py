from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
    bio = db.Column(db.Text, nullable=True)
    date_of_birth = db.Column(db.Date, nullable=True)
    profile_picture = db.Column(db.String(150), nullable=True)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Check if user already exists
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email is already registered. Please log in.')
            return redirect(url_for('login'))
        
        # Validate input data
        is_valid, error_message = validate_signup_data(username, email, password)
        if not is_valid:
            flash(error_message)
            return redirect(url_for('signup'))
        
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Sign Up successful! Please proceed to login.')
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            login_user(user)
            flash('Login successful!')
            return redirect(url_for('profile'))
        else:
            flash('Login Unsuccessful. Please check email and password.')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        current_user.bio = request.form['bio']
        db.session.commit()
        flash('Your profile has been updated!')
        return redirect(url_for('profile'))
    return render_template('profile.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

def validate_signup_data(username, email, password):
    if not username or not email or not password:
        return False, "All fields are required."
    if '@' not in email:
        return False, "Invalid email address."
    return True, ""

if __name__ == '__main__':
    app.run(debug=True)
