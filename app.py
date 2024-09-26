from flask import Flask, render_template, redirect, url_for, request, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import InputRequired

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Set the username and password
users = {'admin': 'admin'}

# Dummy voting results for demonstration purposes
voting_results = {'gs_votes': {'X': 0, 'Y': 0, 'Z': 0},
                  'ags1_votes': {'A': 0, 'B': 0, 'C': 0},
                  'ags2_votes': {'D': 0, 'E': 0, 'F': 0}}

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Register')

@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('index'))

    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        if username not in users:
            users[username] = password
            session['username'] = username
            return redirect(url_for('index'))

    return render_template('register.html', form=form)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/vote', methods=['POST'])
def vote():
    if 'username' in session:
        gs_vote = request.form['gs_vote']
        ags1_vote = request.form['ags1_vote']
        ags2_vote = request.form['ags2_vote']

        # Update voting results
        voting_results['gs_votes'][gs_vote] += 1
        voting_results['ags1_votes'][ags1_vote] += 1
        voting_results['ags2_votes'][ags2_vote] += 1

    return redirect(url_for('results'))

@app.route('/results')
def results():
    return render_template('results.html', gs_votes=voting_results['gs_votes'],
                           ags1_votes=voting_results['ags1_votes'],
                           ags2_votes=voting_results['ags2_votes'])

if __name__ == '__main__':
    app.run(debug=True)
