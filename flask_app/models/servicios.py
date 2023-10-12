import os

from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.usuario import Usuario

class Servicio: 
    def __init__(self, data) -> None:
        self.id = data['id']
        self.nombre = data['nombre']
        self.genero = data['genero']
        self.lugar_creacion = data['lugar_creacion']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.usuario_id = data['usuario_id']
        self.usuario = Usuario.get(data['usuario_id'])

    def json(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "genero": self.genero,
            "lugar_creacion": self.lugar_creacion,
            "usuario_id": self.usuario_id,
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at),
            "usuario": str(self.usuario)
        }

    @classmethod
    def validar_banda(cls, formulario):

        errores = []

        if len(formulario['nombre']) < 2:
            errores.append(
                "Nombre de la banda debe tener al menos 2 caracteres"
            )

        if len(formulario['genero']) < 2:
            errores.append(
                "Género de la banda debe tener al menos 2 caracteres"
            )      
        
        for llave, valor in formulario.items():
            if len(valor) == 0:
                errores.append(
                    f"{llave} no está presente. Dato obligatorio"
                )
        return errores
    
    @classmethod
    def get_all_bands(cls):
        resultados_instancias = []
        query = "SELECT * FROM bands"
        resultados = connectToMySQL(os.getenv('BASE_DATOS')).query_db(query)
        print(resultados)
        for resultado in resultados:
            instancia = cls(resultado)
            resultados_instancias.append(instancia)
        print(resultados_instancias)
        return resultados_instancias
    
    @classmethod
    def save_band(cls, data ):
        query = "INSERT INTO bands (nombre, genero, lugar_creacion, created_at, updated_at, usuario_id) VALUES (%(nombre)s,%(genero)s,%(lugar_creacion)s, NOW(), NOW(),%(usuario_id)s);"
        return connectToMySQL(os.getenv('BASE_DATOS')).query_db( query, data )
    
    @classmethod
    def get_band(cls, id ):
        query = "SELECT * FROM bands WHERE id = %(id)s;"
        data = { 'id': id }
        resultados = connectToMySQL(os.getenv('BASE_DATOS')).query_db( query, data )
        if resultados:
            return cls(resultados[0])
        return None
    
    @classmethod
    def eliminar_banda(cls, id ):
        query = "DELETE FROM bands WHERE id = %(id)s;"
        data = { 'id': id }
        connectToMySQL(os.getenv('BASE_DATOS')).query_db( query, data )
        return True
    
    
    def update_band(self):
        query = "UPDATE bands SET nombre=%(nombre)s,genero=%(genero)s,lugar_creacion=%(lugar_creacion)s,updated_at=NOW() WHERE id = %(id)s;"
        data = {
            'id': self.id,
            'nombre': self.nombre,
            'genero': self.genero,
            'lugar_creacion': self.lugar_creacion
        }
        connectToMySQL(os.getenv('BASE_DATOS')).query_db( query, data )
        return True

    @classmethod
    def get_user_with_bands(cls, usuario_id):
        query = "SELECT * FROM usuario LEFT JOIN bands ON bands.usuario_id = usuario.id WHERE usuario.id = %(id)s;"
        data = {"id" : usuario_id}
        results = connectToMySQL(os.getenv("BASE_DATOS")).query_db(query,data)
        print("RESULTADOS",results)
        if results:
            usuario = Usuario(results[0])
            for row in results:
                        banda_data = {
                            "id" : row["bands.id"],
                            "nombre" : row["bands.nombre"],
                            "genero" : row["genero"],
                            "lugar_creacion" : row["lugar_creacion"],
                            "usuario_id" : row["usuario_id"],
                            "created_at" : row["created_at"],
                            "updated_at" : row["updated_at"],
                        }

                        """usuario.bandas.append(Banda(banda_data))"""
            
            
            return usuario
        return None

    

