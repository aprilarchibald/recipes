from flask_app import app, bcrypt
from flask import render_template, redirect,request, session
from flask_app.models.models_users import User
from flask_app.models.models_recipes import Recipe


@app.route('/')
def index():
    if 's_id' in session:
        return redirect('/dashboard')
    return render_template("index.html")

@app.route('/dashboard')
def dashboard():
    if 's_id' not in session:
        return redirect('/')
    context ={
        'user': User.get_one({'id' : session['s_id']})
    }
    recipes = Recipe.get_all()
    return render_template("dashboard.html", **context, recipes = recipes)

@app.route('/login', methods=["POST"])
def login():
    if not User.login_validator(request.form):
        return redirect('/')
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    del session['s_id']
    return redirect('/')

@app.route('/register', methods=["POST"])
def register():
    if not User.reg_validator(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data ={
        **request.form,
        'password': pw_hash
    }
    id = User.create(data)
    session['s_id'] = id
    return redirect('/dashboard')