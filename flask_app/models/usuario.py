import os

from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.utils.expresiones_regulares import EMAIL_REGEX


class Usuario:
    def __init__(self, data):
        self.id = data['id']
        self.nombre_peluqueria = data['nombre_peluqueria']
        self.direccion = data['direccion']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    def __str__(self) -> str:
        return f"{self.email} ({self.id})"

    @classmethod
    def validar(cls, formulario):

        errores = []
        if not EMAIL_REGEX.match(formulario['email']):
            errores.append(
                "El correo indicado es inválido"
            )

        if cls.get_by_email(formulario['email']):
            errores.append(
                "El correo ya existe"
            )
        if len(formulario['nombre_peluqueria']) < 2:
            errores.append(
                "Nombre del Local debe tener al menos 2 caracteres"
            )

        if len(formulario['direccion']) < 2:
            errores.append(
                "Direccion debe tener al menos 2 caracteres"
            )

        
        if len(formulario['password']) < 8:
            errores.append(
                "Contraseña debe tener al menos 8 caracteres"
            )

        for llave, valor in formulario.items():
            if len(valor) == 0:
                errores.append(
                    f"{llave} no está presente. Dato obligatorio"
                )
        return errores

    @classmethod
    def get_all(cls):
        resultados_instancias = []
        query = "SELECT * FROM usuario"
        resultados = connectToMySQL(os.getenv('BASE_DATOS')).query_db(query)
        for resultado in resultados:
            instancia = cls(resultado)
            resultados_instancias.append(instancia)

        return resultados_instancias

    @classmethod
    def save(cls, data ):
        query = "INSERT INTO usuario (nombre_peluqueria, direccion, email, password, created_at, updated_at) VALUES (%(nombre_peluqueria)s,%(direccion)s,%(email)s, %(password)s, NOW(), NOW());"
        return connectToMySQL(os.getenv('BASE_DATOS')).query_db( query, data )
    
    @classmethod
    def get(cls, id ):
        query = "SELECT * FROM usuario WHERE id = %(id)s;"
        data = { 'id': id }
        resultados = connectToMySQL(os.getenv('BASE_DATOS')).query_db( query, data )
        if resultados:
            return cls(resultados[0])
        
        return None
    
    @classmethod
    def get_by_email(cls, email ):
        query = "SELECT * FROM usuario WHERE email = %(email)s;"
        data = { 'email': email }
        resultados = connectToMySQL(os.getenv('BASE_DATOS')).query_db( query, data )
        if resultados:
            return cls(resultados[0])
        
        return None
    
    
    @classmethod
    def eliminar(cls, id ):
        query = "DELETE FROM usuario WHERE id = %(id)s;"
        data = { 'id': id }
        connectToMySQL(os.getenv('BASE_DATOS')).query_db( query, data )
        return True
    
    def update(self):
        query = "UPDATE usuario SET password = %(password)s, updated_at = NOW() WHERE id = %(id)s"
        data = {
            'id': self.id,
            'password': self.password
        }
        connectToMySQL(os.getenv('BASE_DATOS')).query_db( query, data )
        return True
