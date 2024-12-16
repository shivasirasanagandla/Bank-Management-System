from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(__name__)
app.secret_key = 'secretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bank.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    bank_name = db.Column(db.String(100), nullable=False)
    balance = db.Column(db.Float, default=0.0)
@app.route('/')
def home():
    return render_template('home.html')
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        bank_name = request.form['bank_name']
        if User.query.filter_by(username=username).first():
            flash('Username already exists!', 'danger')
            return redirect(url_for('register'))
        new_user = User(username=username, password=password, bank_name=bank_name)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        bank_name = request.form['bank_name']
        user = User.query.filter_by(username=username, bank_name=bank_name).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['bank_name'] = user.bank_name
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials!', 'danger')
    return render_template('login.html')
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please log in first!', 'warning')
        return redirect(url_for('login'))
    username = session['username']
    bank_name = session['bank_name']
    return render_template('dashboard.html', username=username, bank_name=bank_name)
@app.route('/deposit', methods=['POST'])
def deposit():
    if 'user_id' not in session:
        flash('Please log in first!', 'warning')
        return redirect(url_for('login'))
    amount = float(request.form['amount'])
    user = User.query.get(session['user_id'])
    user.balance += amount
    db.session.commit()
    flash(f'Deposited {amount} successfully!', 'success')
    return redirect(url_for('dashboard'))
@app.route('/withdraw', methods=['POST'])
def withdraw():
    if 'user_id' not in session:
        flash('Please log in first!', 'warning')
        return redirect(url_for('login'))
    amount = float(request.form['amount'])
    user = User.query.get(session['user_id'])
    if amount > user.balance:
        flash('Insufficient balance!', 'danger')
    else:
        user.balance -= amount
        db.session.commit()
        flash(f'Withdraw {amount} successfully!', 'success')
    return redirect(url_for('dashboard'))
@app.route('/balance')
def balance():
    if 'user_id' not in session:
        flash('Please log in first!', 'warning')
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    return render_template('balance.html', balance=user.balance)
@app.route('/account_details')
def account_details():
    if 'user_id' not in session:
        flash('Please log in first!', 'warning')
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    return render_template('account_details.html', user=user)
@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully!', 'info')
    return redirect(url_for('home'))
if __name__ == '__main__':
    with app.app_context():
        db.create_all() 
    app.run(debug=True)
