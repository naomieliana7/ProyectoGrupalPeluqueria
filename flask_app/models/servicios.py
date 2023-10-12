import os

from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.usuario import Usuario

class Servicio:
    def __init__(self, data):
        self.id = data['id']
        self.nombre_servicio = data['nombre_servicio']
        self.precio = data['precio']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.usuario = Usuario.get(data['usuario_id'])

    def json(self):
        return {
            "id": self.id,
            "nombre_servicio": self.nombre_servicio,
            "precio": self.precio,
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at),
            
        }


    @classmethod
    def validar_servicio(cls, formulario):

        errores = []
                
        if len(formulario['nombre_servicio']) < 5:
            errores.append(
                "Nombre del servicio debe tener al menos 3 caracteres"
            )

        if len(formulario['precio']) == 0 or len(formulario['precio']) < 0 :
            errores.append(
                "Precio no puede ser 0"
            )

        for llave, valor in formulario.items():
            if len(valor) == 0:
                errores.append(
                    f"{llave} no está presente. Dato obligatorio"
                )
        return errores

    @classmethod
    def get_all_servicios(cls):
        resultados_instancias = []
        query = "SELECT * FROM servicios"
        resultados = connectToMySQL(os.getenv('BASE_DATOS')).query_db(query)
        for resultado in resultados:
            instancia = cls(resultado)
            resultados_instancias.append(instancia)

        return resultados_instancias

    @classmethod
    def save_servicio(cls, data ):
        query = "INSERT INTO servicios (nombre_servicio, precio, created_at, updated_at) VALUES (%(nombre_servicio)s,%(precio)s, NOW(), NOW());"
        return connectToMySQL(os.getenv('BASE_DATOS')).query_db( query, data )
    
    @classmethod
    def get_servicio(cls, id ):
        query = "SELECT * FROM servicios WHERE id = %(id)s;"
        data = { 'id': id }
        resultados = connectToMySQL(os.getenv('BASE_DATOS')).query_db( query, data )
        if resultados:
            return cls(resultados[0])
        
        return None
    
    
    @classmethod
    def eliminar_servicio(cls, id ):
        query = "DELETE FROM servicios WHERE id = %(id)s;"
        data = { 'id': id }
        connectToMySQL(os.getenv('BASE_DATOS')).query_db( query, data )
        return True

    @classmethod
    def update_servicio(self):
        query = "UPDATE servicios SET nombre_servicio=%(nombre_servicio)s,precio=%(precio)s,updated_at=NOW() WHERE id = %(id)s;"
        data = {
            'id': self.id,
            'nombre_servicio': self.nombre_servicio,
            'precio': self.precio
        }
        connectToMySQL(os.getenv('BASE_DATOS')).query_db( query, data )
        return True
    
    
    

