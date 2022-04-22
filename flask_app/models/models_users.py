from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE, bcrypt
from flask import flash,session
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 


class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create(cls, data:dict):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s);"
        user_id= connectToMySQL(DATABASE).query_db( query, data )
        return user_id 

    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(DATABASE).query_db(query)
        if results:
            users = []
            for user in results:
                users.append( cls(user) )
            return users
        return False

    @classmethod
    def get_one(cls,data:dict):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result= connectToMySQL(DATABASE).query_db( query, data )
        if result:
            return cls(result[0])
        return False

    @classmethod
    def get_one_by_email(cls,data:dict):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result= connectToMySQL(DATABASE).query_db( query, data )
        if result:
            return cls(result[0])
        return False
    
    @staticmethod
    def login_validator(form_data: dict):
        is_valid = True
        if len(form_data['email']) < 1:
            flash('Email is a required field', 'err_email_login')
            is_valid = False
        elif not EMAIL_REGEX.match(form_data['email']): 
            flash("Invalid email address!", 'err_email')
            is_valid = False
        if len(form_data['password']) <= 1:
            flash('Password is a required field', 'err_password_login')
            is_valid = False
        if is_valid:
            potential_user = User.get_one_by_email({'email': form_data['email']})
            if potential_user:
                if not bcrypt.check_password_hash(potential_user.password, form_data['password']):
                    is_valid = False
                    flash('Invalid entry', 'err_confirm_pw_login')
                else:
                    session['s_id'] = potential_user.id
            else: 
                flash('Invalid entry', 'err_confirm_pw_login')
                is_valid = False
        return is_valid

    @staticmethod
    def reg_validator(form_data: dict):
        is_valid = True
        if len(form_data['first_name']) <= 2:
            flash('First name is a required field', 'err_first_name')
            is_valid = False
        if len(form_data['last_name']) <= 2:
            flash('Last Name is a required field', 'err_last_name')
            is_valid = False
        if len(form_data['email']) <= 0:
            flash('Email is a required field!', 'err_email')
            is_valid = False
        elif not EMAIL_REGEX.match(form_data['email']): 
            flash("Invalid email address!", 'err_email')
            is_valid = False
        else:
            potential_user = User.get_one_by_email({'email': form_data['email']})
            if potential_user: 
                flash('Email is already taken!', 'err_email')
                is_valid = False
        if len(form_data['password']) < 1:
            flash('Password is a required field', 'err_password')
            is_valid = False
        if len(form_data['confirm_pw']) < 1:
            flash('Confirm password is a required field', 'err_confirm_pw')
            is_valid = False
        elif form_data['password'] != form_data['confirm_pw']:
            is_valid = False
            flash('Passwords do not match', 'err_confirm_pw')
        return is_valid