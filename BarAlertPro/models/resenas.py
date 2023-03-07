from BarAlertPro.config.mysqlconnection import connectToMySQL
from flask import flash

class Resenas:
    def __init__(self, data):
        self.id_resenas = data['id_resenas']
        self.puntaje_resena = data['puntaje_resena']
        self.comentario_resena = data['comentario_resena']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls,data):
        query = "insert into resenas (puntaje_resena, comentario_resena, created_at, updated_at, users_id_user, bares_id_bares) values (%(puntaje_resena)s, %(comentario_resena)s, now(), now(), %(users_id_user)s, %(bares_id_bares)s);"
        result = connectToMySQL('bar-alert-pro').query_db(query, data)
        data_user = {
            "id" : result
        }
        return cls.get_Id(data_user)
    
    @classmethod
    def get_Id(cls,data):
        query = "select * from resenas where id_resenas = %(id)s;"
        print(query)
        result = connectToMySQL('bar-alert-pro').query_db(query, data)
        if len(result) > 0:
            return cls(result[0])
        else:
            return None
        
    @staticmethod
    def validate_resena(resena):
        is_valid = True
        if len(resena['comentario_resena']) < 20:
            flash("La reseña debe tener por lo menos 20 caracteres")
            is_valid = False
        return is_valid