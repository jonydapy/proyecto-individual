from BarAlertPro.config.mysqlconnection import connectToMySQL
from flask import flash
import re

# Para poder validar el correo
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Bar:
    def __init__(self, data):
        self.id_bares = data['id_bares']
        self.nombre_bar = data['nombre_bar']
        self.email_bar = data['email_bar']
        self.bar_password = data['bar_password']
        self.link_menu = data['link_menu']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.resenas = []
        self.aportes = []

    @classmethod
    def get_all_bares(cls):
        query = "select * from bares;"
        results = connectToMySQL('bar-alert-pro').query_db(query)
        bares = []
        for result in results:
            bares.append( cls(result) )
        return bares
    
    @classmethod
    def save(cls,data):
        query = "INSERT INTO bares (nombre_bar, email_bar, bar_password, link_menu, created_at, updated_at) VALUES (%(nombre_bar)s, %(email_bar)s, %(bar_password)s, %(link_menu)s, now(), now());"
        result = connectToMySQL('bar-alert-pro').query_db(query, data)
        data_user = {
            "id" : result
        }
        return cls.get_Id(data_user)
    
    @classmethod
    def get_Id(cls,data):
        query = "select * from bares where id_bares = %(id)s;"
        print(query)
        result = connectToMySQL('bar-alert-pro').query_db(query, data)
        if len(result) > 0:
            return cls(result[0])
        else:
            return None
        
    @classmethod
    def get_Email(cls, email):
        query = "select * from bares where email_bar = %(email_bar)s;"
        data = {
            'email_bar': email
        }
        result = connectToMySQL('bar-alert-pro').query_db(query, data)
        if len(result) > 0:
            return cls(result[0])
        else:
            return None
        
    @classmethod
    def get_bar_promo_precio(cls,data):
        query = "select bares.id_bares as id_bares, bares.nombre_bar as nombre_bar, promos.nombre_promo as nombre_promo, promos.precio_promo as precio_promo, bares.link_menu as link_menu, bares.ubicacion as ubicacion from bares left join promos on bares.id_bares = promos.bares_id_bares where promos.bares_id_bares = %(id_bares)s limit 1;"
        result = connectToMySQL('bar-alert-pro').query_db(query,data)
        print(result)
        return result

# Area de Validaciones
    @staticmethod
    def validate_user(usuario):
        is_valid = True
        if len(usuario['nombre_bar']) < 3:
            flash("El nombre debe tener por lo menos 3 caracteres")
            is_valid = False
        if not EMAIL_REGEX.match(usuario['email_bar']): 
            flash("Direccion de email invalida!")
            is_valid = False
        if len(usuario['bar_password']) < 8:
            flash("La contraseña debe tener por lo menos 8 caracteres")
            is_valid = False
        return is_valid