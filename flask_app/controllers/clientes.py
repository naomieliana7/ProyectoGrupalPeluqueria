from flask import flash, redirect, request, session, render_template, jsonify
from flask_app.models.clientes import Cliente
from flask_app.models.usuario import Usuario

from flask_app import app

@app.route('/procesar_cliente', methods=["POST"])
def procesar_cliente():
    print(request.form)

    errores = Cliente.validar_cliente(request.form)
    if len(errores) > 0:
        for error in errores:
            flash(error, "error")
        return redirect("/")

    data = {
        'nombre_apellido': request.form["nombre_apellido"],
        'direccion': request.form["direccion"],
        'telefono': request.form["telefono"],
        'correo': request.form["correo"],
        'usuario_id': session['usuario_id']

    }
    print(data)
    id = Cliente.save_cliente(data)
    print(id)
    flash( "Cliente añadido", "success")

    return redirect("/clientes/<id>")

@app.route('/nuevo_cliente')
def nuevo():
    if not session.get('usuario_id'):
        flash("No estás logeado!!!!", "error")
        return redirect("/login")

    user_in_session = Usuario.get(session['usuario_id'])
    
    return render_template('nuevo_cliente.html', user_in_session=user_in_session)


@app.route('/clientes/<id>')
def clientes(id):
    print('HHHHHHHH')
    clientes = Cliente.get_all_clientes()
    user_in_session = Usuario.get(session['usuario_id'])
    return render_template('clientes.html', clientes=clientes, user_in_session=user_in_session)


@app.route('/editar_cliente/<id>')
def editar(id):
    user_in_session = Usuario.get(session['usuario_id'])
    cliente = Cliente.get_cliente(id)
    return render_template('editar_cliente.html', cliente=cliente, user_in_session=user_in_session)

@app.route('/procesar_cliente_editar/<id>', methods=["POST"])
def procesar_cliente_editar(id):
    print(request.form)
    print('EDITAR')
    errores = Cliente.validar_cliente(request.form)
    if len(errores) > 0:
        for error in errores:
            flash(error, "error")
        return redirect("/")
    cliente = Cliente.get_cliente(id)

    cliente.nombre_apellido = request.form['nombre_apellido']
    cliente.direccion = request.form['direccion']
    cliente.telefono = request.form['telefono']
    cliente.correo = request.form['correo']

    cliente.update_cliente()
    
    flash( "Datos del cliente editados", "success")

    return redirect("/clientes/<id>")



@app.route('/eliminar/<id>')
def eliminar(id):
    Cliente.eliminar_cliente(id)
    return redirect('/clientes/<id>')
