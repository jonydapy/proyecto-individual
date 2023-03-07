from BarAlertPro.config.mysqlconnection import connectToMySQL
from flask import flash
import re

# Para poder validar el correo
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id_user = data['id_user']
        self.nickname = data['nickname']
        self.email_user = data['email_user']
        self.user_password = data['user_password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.resenas = []
        self.aportes = []

    @classmethod
    def get_all_users(cls):
        query = "select * from users;"
        results = connectToMySQL('bar-alert-pro').query_db(query)
        users = []
        for result in results:
            users.append( cls(result) )
        return users
    
    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (nickname, email_user, user_password, created_at, updated_at) VALUES (%(nickname)s, %(email_user)s, %(user_password)s, now(), now());"
        result = connectToMySQL('bar-alert-pro').query_db(query, data)
        data_user = {
            "id" : result
        }
        return cls.get_Id(data_user)
    
    @classmethod
    def get_Id(cls,data):
        query = "select * from users where id_user = %(id)s;"
        print(query)
        result = connectToMySQL('bar-alert-pro').query_db(query, data)
        if len(result) > 0:
            return cls(result[0])
        else:
            return None
        
    @classmethod
    def get_Email(cls, email):
        query = "select * from users where email_user = %(email_user)s;"
        data = {
            'email_user': email
        }
        result = connectToMySQL('bar-alert-pro').query_db(query, data)
        if len(result) > 0:
            return cls(result[0])
        else:
            return None
        
    @classmethod
    def update(cls,data):
        query = "UPDATE users SET nickname=%(nickname)s, email_user=%(email_user)s, updated_at=NOW() WHERE id_user = %(id_user)s;"
        return connectToMySQL('bar-alert-pro').query_db(query, data)

# Area de Validaciones
    @staticmethod
    def validate_user(usuario):
        is_valid = True
        if len(usuario['nickname']) < 3:
            flash("El nombre debe tener por lo menos 3 caracteres")
            is_valid = False
        if not EMAIL_REGEX.match(usuario['email_user']): 
            flash("Direccion de email invalida!")
            is_valid = False
        if len(usuario['user_password']) < 8:
            flash("La contraseña debe tener por lo menos 8 caracteres")
            is_valid = False
        return is_valid
    
    @staticmethod
    def update_user_val(usuario):
        is_valid = True
        if len(usuario['nickname']) < 3:
            flash("Tu nombre de usuario debe tener al menos 3 caracteres")
            is_valid = False
        if not EMAIL_REGEX.match(usuario['email_user']): 
            flash("Ingresa un correo válido!")
            is_valid = False
        return is_valid
    
# Obtener datos del usuario por ID
    @classmethod
    def get_resenas_por_id(cls,data):
        query = "SELECT * FROM resenas WHERE users_id_user = %(users_id_user)s;"
        result = connectToMySQL('bar-alert-pro').query_db(query,data)
        print(result)
        return result
    
    @classmethod
    def get_aportes_por_id(cls,data):
        query = "SELECT * FROM promos WHERE users_id_user = %(users_id_user)s;"
        result = connectToMySQL('bar-alert-pro').query_db(query,data)
        print(result)
        return result

# Obtener datos join
    @classmethod
    def get_bar_promo_precio(cls,data):
        query = "select users.id_user as id_user, bares.nombre_bar as nombre_bar, promos.nombre_promo as nombre_promo, promos.precio_promo as precio_promo from users left join promos on users.id_user = promos.users_id_user left join bares on bares.id_bares = promos.bares_id_bares  where promos.users_id_user = %(id_user)s;"
        result = connectToMySQL('bar-alert-pro').query_db(query,data)
        print(result)
        return result
