from BarAlertPro.config.mysqlconnection import connectToMySQL
from flask import flash

class Promo:
    def __init__(self,data):
        self.id_promos = data['id_promos']
        self.nombre_promo = data['nombre_promo']
        self.bares_id_bares = data['bares_id_bares']
        self.users_id_user = data['users_id_user'] 
        self.precio_promo = data['precio_promo']
        self.bebida_tipo = data['bebida_tipo']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all_promos(cls):
        query = "select * from promos;"
        results = connectToMySQL('bar-alert-pro').query_db(query)
        promos = []
        for result in results:
            promos.append( cls(result) )
        return promos
    
    @classmethod
    def save(cls,data):
        query = "insert into promos (nombre_promo, precio_promo, bebida_tipo, created_at, updated_at, users_id_user, bares_id_bares) values (%(nombre_promo)s, %(precio_promo)s, %(bebida_tipo)s, now(), now(), %(users_id_user)s, %(bares_id_bares)s);"
        result = connectToMySQL('bar-alert-pro').query_db(query, data)
        data_user = {
            "id" : result
        }
        return cls.get_Id(data_user)
    
    @classmethod
    def get_Id(cls,data):
        query = "select * from promos where id_promos = %(id)s;"
        print(query)
        result = connectToMySQL('bar-alert-pro').query_db(query, data)
        if len(result) > 0:
            return cls(result[0])
        else:
            return None
        
    @classmethod
    def get_bar_ubi_promo_precio_home(cls):
        query = "select bares.id_bares as id_bares, bares.nombre_bar as nombre_bar,bares.ubicacion as ubicacion,promos.nombre_promo as nombre_promo, promos.precio_promo as precio_promo from bares left join promos on bares.id_bares = promos.bares_id_bares limit 3;"
        results = connectToMySQL('bar-alert-pro').query_db(query)
        print("*****************aqui llegamos" , results)
        promos = []
        for result in results:
            promo_data = {
                "id_bares" : result['id_bares'],
                "nombre_bar" : result['nombre_bar'],
                "ubicacion" : result['ubicacion'],
                "nombre_promo" : result['nombre_promo'],
                "precio_promo" : result['precio_promo']
            }
            promos.append( promo_data )
        return promos
    
    @classmethod
    def get_bar_promo_precio(cls):
        query = "SELECT bares.id_bares AS id_bares, bares.nombre_bar AS nombre_bar, bares.ubicacion AS ubicacion, promos.nombre_promo AS nombre_promo, promos.precio_promo AS precio_promo FROM bares LEFT JOIN promos ON bares.id_bares = promos.bares_id_bares ORDER BY promos.created_at DESC LIMIT 8;"
        results = connectToMySQL('bar-alert-pro').query_db(query)
        print("*****************aqui llegamos" , results)
        promos = []
        for result in results:
            promo_data = {
                "id_bares" : result['id_bares'],
                "nombre_bar" : result['nombre_bar'],
                "ubicacion" : result['ubicacion'],
                "nombre_promo" : result['nombre_promo'],
                "precio_promo" : result['precio_promo']
            }
            promos.append( promo_data )
        return promos

    # Area de validaciones

    @staticmethod
    def validate_promo(promocion):
        is_valid = True
        if len(promocion['nombre_promo']) < 3:
            flash("El nombre debe tener por lo menos 3 caracteres")
            is_valid = False
        if int(promocion['precio_promo']) < 5000:
            flash("El precio debe ser mayor a Gs. 5000")
            is_valid = False
        return is_valid