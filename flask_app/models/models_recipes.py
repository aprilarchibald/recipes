from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash,session
from flask_app.models import models_users



class Recipe:
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_made = data['date_made']
        self.under_30_min = data['under_30_min']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        # self.created_by = User.get_one({'id': data['user_id']})



    @classmethod
    def create(cls, data:dict):
        query = "INSERT INTO recipes (name, description, instructions, date_made, under_30_min, user_id) VALUES (%(name)s,%(description)s,%(instructions)s,%(date_made)s, %(under_30_min)s, %(user_id)s);"
        recipe_id= connectToMySQL(DATABASE).query_db( query, data )
        return recipe_id

    

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes LEFT JOIN users ON users.id = recipes.user_id;"
        results = connectToMySQL(DATABASE).query_db(query)
        if results:
            recipes = []
            for row in results:
                recipe = cls(row)
                user_dict ={
                    **row, 
                    'id': row['users.id'],
                    'created_at' : row['users.created_at'],
                    'updated_at' : row['users.updated_at']
                }
                recipe.created_by = models_users.User(user_dict)
                recipes.append(recipe)
            return recipes
        return []

    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM recipes LEFT JOIN users ON users.id = recipes.user_id WHERE recipes.id = %(id)s;"
        result= connectToMySQL(DATABASE).query_db( query, data )
        if result:
            recipe = cls(result[0])
            user_dict ={
                **result[0], 
                'id': result[0]['users.id'],
                'created_at' : result[0]['users.created_at'],
                'updated_at' : result[0]['users.updated_at']
            }
            recipe.created_by = models_users.User(user_dict)
            return recipe
        return False

    @classmethod
    def update(cls, data):
        query= "UPDATE recipes SET name= %(name)s, description = %(description)s, instructions = %(instructions)s, date_made= %(date_made)s, under_30_min = %(under_30_min)s WHERE id =%(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def delete(cls, data:dict):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db( query, data)



    @staticmethod
    def validator(form_data: dict):
        is_valid = True
        if len(form_data['name']) < 3:
            flash('Name is a required field', 'err_name')
            is_valid = False
        if len(form_data['description']) < 3: 
            flash("Description is a required field!", 'err_description')
            is_valid = False
        if len(form_data['instructions']) < 3:
            flash('Instructions is a required field', 'err_instructions')
            is_valid = False
        if len(form_data['date_made']) < 1:
            flash('Please fill out date', 'err_date_made')
            is_valid = False
        if not "under_30_min" in form_data:
            flash('Please fill out time limit', 'err_under_30_min')
            is_valid = False
        return is_valid

