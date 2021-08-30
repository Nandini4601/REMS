from flask import render_template, flash, redirect, url_for
from rems import app
from rems.forms import LoginForm


@app.route('/')
@app.route('/home')
def index():
    return render_template('homepage.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Fill all fields for user {} '.format(form.username.data))
        return redirect(url_for('home2'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/home2')
def home2():
    return render_template('index.html')
