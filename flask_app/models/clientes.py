import os

from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.usuario import Usuario
from flask_app.utils.expresiones_regulares import EMAIL_REGEX, TELEFONO_PY_REGEX

class Cliente:
    def __init__(self, data):
        self.id = data['id']
        self.nombre_apellido = data['nombre_apellido']
        self.direccion = data['direccion']
        self.telefono = data['telefono']
        self.correo = data['correo']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.usuario_id = data['usuario_id']
        self.usuario = Usuario.get(data['usuario_id'])

    def json(self):
        return {
            "id": self.id,
            "nombre_apellido": self.nombre_apellido,
            "direccion": self.direccion,
            "telefono": self.telefono,
            "correo": self.correo,
            "usuario_id": self.usuario_id,
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at),
            "usuario": str(self.usuario)
        }


    @classmethod
    def validar_cliente(cls, formulario):

        errores = []
        if not EMAIL_REGEX.match(formulario['correo']):
            errores.append(
                "El correo indicado es inválido"
            )

        if cls.get_cliente_by_email(formulario['correo']):
            errores.append(
                "El correo ya existe"
            )
        if len(formulario['nombre_apellido']) < 5:
            errores.append(
                "Nombre y Apellido debe tener al menos 5 caracteres"
            )

        if len(formulario['direccion']) < 2:
            errores.append(
                "Direccion debe tener al menos 2 caracteres"
            )

        for llave, valor in formulario.items():
            if len(valor) == 0:
                errores.append(
                    f"{llave} no está presente. Dato obligatorio"
                )
        return errores

    @classmethod
    def get_all_clientes(cls):
        resultados_instancias = []
        query = "SELECT * FROM clientes"
        resultados = connectToMySQL(os.getenv('BASE_DATOS')).query_db(query)
        for resultado in resultados:
            instancia = cls(resultado)
            resultados_instancias.append(instancia)

        return resultados_instancias

    @classmethod
    def save_cliente(cls, data ):
        query = "INSERT INTO clientes (nombre_apellido, direccion,telefono, correo, created_at, updated_at, usuario_id) VALUES (%(nombre_apellido)s,%(direccion)s,%(telefono)s, %(correo)s, NOW(), NOW(),%(usuario_id)s);"
        return connectToMySQL(os.getenv('BASE_DATOS')).query_db( query, data )
    
    @classmethod
    def get_cliente(cls, id ):
        query = "SELECT * FROM clientes WHERE id = %(id)s;"
        data = { 'id': id }
        resultados = connectToMySQL(os.getenv('BASE_DATOS')).query_db( query, data )
        if resultados:
            return cls(resultados[0])
        
        return None
    
    @classmethod
    def get_cliente_by_email(cls, email ):
        query = "SELECT * FROM cliente WHERE correo = %(correo)s;"
        data = { 'email': email }
        resultados = connectToMySQL(os.getenv('BASE_DATOS')).query_db( query, data )
        if resultados:
            return cls(resultados[0])
        
        return None
    @classmethod
    def eliminar_cliente(cls, id ):
        query = "DELETE FROM clientes WHERE id = %(id)s;"
        data = { 'id': id }
        connectToMySQL(os.getenv('BASE_DATOS')).query_db( query, data )
        return True

    @classmethod
    def update_cliente(self):
        query = "UPDATE clientes SET nombre_apellido=%(nombre_apellido)s,direccion=%(direccion)s,telefono=%(telefono)s,correo=%(correo)s,updated_at=NOW() WHERE id = %(id)s;"
        data = {
            'id': self.id,
            'nombre_apellido': self.nombre_apellido,
            'direccion': self.direccion,
            'telefono': self.telefono,
            'correo': self.correo
        }
        connectToMySQL(os.getenv('BASE_DATOS')).query_db( query, data )
        return True
    
    @classmethod
    def get_user_with_clientes(cls, usuario_id):
        query = "SELECT * FROM clientes WHERE usuario_id = %(id)s;"
        data = {"id": usuario_id}
        resultados = connectToMySQL(os.getenv("BASE_DATOS")).query_db(query, data)

        clientes_del_usuario = []
        for resultado in resultados:
            instancia = cls(resultado)
            clientes_del_usuario.append(instancia)

        return clientes_del_usuario