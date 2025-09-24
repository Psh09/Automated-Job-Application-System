from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import yaml
from easy_apply_bot import EasyApplyBot

app = Flask(__name__)
#app.config['SECRET_KEY'] = 'secret_key_here'

# Load config from YAML file
with open("config.yaml", 'r') as stream:
    config = yaml.safe_load(stream)

# Create a simple user class
class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

# Create a login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Load user from config
user = User(1, config['username'], config['password'])

@login_manager.user_loader
def load_user(user_id):
    return user

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == user.username and user.check_password(password):
            login_user(user)
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))




if __name__ == '__main__':
    app.run(debug=True)

@app.route('/dashboard', methods=['POST'])
@login_required
def dashboard():
    positions = request.form['positions']
    locations = request.form['locations']
    salary = request.form['salary']
    rate = request.form['rate']
    bot = EasyApplyBot(config['username'], config['password'], config['phone_number'], salary, rate, uploads=config['uploads'], filename=config['output_filename'], blacklist=config['blacklist'], blackListTitles=config['blackListTitles'], experience_level=config['experience_level'])
    bot.start_apply(positions, locations)