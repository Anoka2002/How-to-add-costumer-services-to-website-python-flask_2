from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Secret key for flash messages

# Route for the home page
@app.route('/')
def home():
    return render_template('index.html')

# Route for sign up
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Validate input data
        is_valid, error_message = validate_signup_data(username, email, password)
        if not is_valid:
            flash(error_message)
            return redirect(url_for('signup'))
        
        # Add user to the database (assuming user addition logic here)
        
        flash('Sign Up successful! Please proceed to purchase.')
        return redirect(url_for('purchase'))
    return render_template('signup.html')

# Route for login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Verify user credentials (assuming verification logic here)
        
        flash('Login successful!')
        return redirect(url_for('home'))
    return render_template('login.html')

# Route for purchase
@app.route('/purchase')
def purchase():
    return render_template('purchase.html')

# Function to validate sign-up data
def validate_signup_data(username, email, password):
    if not username or not email or not password:
        return False, "All fields are required."
    if '@' not in email:
        return False, "Invalid email address."
    return True, ""

if __name__ == '__main__':
    app.run(debug=True)