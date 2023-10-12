from flask import flash, redirect, request, session, render_template, jsonify
from flask_app.models.servicios import Servicio
from flask_app.models.clientes import Cliente
from flask_app.models.usuario import Usuario

from flask_app import app

@app.route('/procesar_servicio', methods=["POST"])
def procesar_servicio():
    print(request.form)

    errores = Servicio.validar_servicio(request.form)
    if len(errores) > 0:
        for error in errores:
            flash(error, "error")
        return redirect("/inicio")

    data = {
        'nombre_servicio': request.form["nombre_servicio"],
        'precio': request.form["precio"],

    }
    print(data)
    id = Servicio.save_servicio(data)
    print(id)
    flash( "Servicio añadido", "success")

    return redirect("/servicios/<id>")

@app.route('/nuevo_servicio')
def nuevo():
    if not session.get('usuario_id'):
        flash("No estás logeado!!!!", "error")
        return redirect("/login")

    user_in_session = Usuario.get(session['usuario_id'])
    
    return render_template('nuevo_servicio.html', user_in_session=user_in_session)


@app.route('/servicios')
def servicios():
    print('HHHHHHHH')
    servicios = Servicio.get_all_servicios()
    user_in_session = Usuario.get(session['usuario_id'])
    return render_template('servicios.html', servicios=servicios, user_in_session=user_in_session)

@app.route('/eliminar/<id>')
def eliminar(id):
    Servicio.eliminar_servicios(id)
    return redirect('/servicios/<id>')