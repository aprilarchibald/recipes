from flask_app import app
from flask import render_template, redirect,request, session
from flask_app.models import models_recipes, models_users



@app.route("/recipes/new")
def enter_info():
    return render_template("enter_new.html")

@app.route('/create/new', methods=["POST"])
def create_new_recipe():
    if not models_recipes.Recipe.validator(request.form):
        return redirect('/recipes/new')
    data={
        **request.form,
        "user_id" : session['s_id']
    }
    models_recipes.Recipe.create(data)
    return redirect('/dashboard')

@app.route('/view/<int:id>')
def view_instructions(id):
    context ={
        'user': models_users.User.get_one({'id' : session['s_id']})
    }
    data ={
        "id":id
    }
    recipe =models_recipes.Recipe.get_one(data)
    return render_template("view.html", recipe=recipe, **context)

@app.route('/edit/<int:id>')
def edit(id):
    data={
        "id":id
    }
    return render_template("edit.html", recipe=models_recipes.Recipe.get_one(data))

@app.route('/update/<int:id>', methods =["POST"])
def update(id):
    if not models_recipes.Recipe.validator(request.form):
        return redirect(f'/edit/{id}')
    # if session['s_id'] == models_recipes.Recipe.user_id:
        # return redirect('/dashboard')
    data={
        **request.form, 
        "id":id
    }
    models_recipes.Recipe.update(data)
    return redirect('/dashboard') 

@app.route('/delete/<int:id>')
def delete(id):
    models_recipes.Recipe.delete({'id': id})
    return redirect('/dashboard')









