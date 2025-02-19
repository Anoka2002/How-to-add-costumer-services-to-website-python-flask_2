from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User, Subscription, Post
from app.forms import RegistrationForm, LoginForm, UpdateAccountForm
from sqlalchemy.exc import IntegrityError

main = Blueprint('main', __name__)

@main.route('/')
def home():
    posts = Post.query.all()
    return render_template('index.html', posts=posts)

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.dashboard'))
        flash('Login unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        try:
            db.session.commit()
            flash('Your account has been created! You can now log in', 'success')
            return redirect(url_for('main.login'))
        except IntegrityError:
            db.session.rollback()
            flash('Username or Email already exists. Please try again with different details.', 'danger')
    return render_template('register.html', title='Register', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.home'))

@main.route('/dashboard')
@login_required
def dashboard():
    subscription = Subscription.query.filter_by(user_id=current_user.id).first()
    return render_template('dashboard.html', subscription=subscription)

@main.route('/purchase', methods=['GET', 'POST'])
@login_required
def purchase():
    if request.method == 'POST':
        plan = request.form.get('plan')
        duration = int(request.form.get('duration'))
        if plan and duration:
            new_subscription = Subscription(user_id=current_user.id, plan=plan, duration=duration)
            db.session.add(new_subscription)
            db.session.commit()
            flash('Subscription purchased successfully!', 'success')
            return redirect(url_for('main.dashboard'))
    return render_template('purchase.html')

@main.route('/premium-content')
@login_required
def premium_content():
    return render_template('premium_content.html')

@main.route('/basic-content')
@login_required
def basic_content():
    return render_template('basic_content.html')

@main.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.image_file = form.picture.data
        current_user.bio = form.bio.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('main.profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.picture.data = current_user.image_file
        form.bio.data = current_user.bio
    return render_template('profile.html', title='Account', form=form)

@main.route('/about')
def about():
    return render_template('about.html', title='About')

@main.route('/contact')
def contact():
    return render_template('contact.html', title='Contact')