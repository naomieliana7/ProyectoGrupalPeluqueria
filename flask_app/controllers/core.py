from flask import render_template, flash, redirect, session
from flask_app import app
from flask_app.models.usuario import Usuario



@app.route('/')
def inicio():
    
    if not session.get('usuario_id'):
        flash("No estás logeado!!!!", "error")
        return redirect("/login")

    user_in_session = Usuario.get(session['usuario_id'])
    
    return render_template(
        'inicio.html',
        usuario=user_in_session,
        user_in_session=user_in_session  
    )