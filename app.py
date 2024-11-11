from flask import Flask, render_template, request, flash
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'  # Necesaria para las funciones de flash

# Configuración de la base de datos
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'paginawebwm',
    'raise_on_warnings': True,
    'use_pure': True,
}


@app.route('/')
def inicio():
    return render_template('Sitio/index.html')

@app.route('/proyectos')
def proyectos():
    return render_template('Sitio/proyectos.html')

@app.route('/sobrenosotros')
def sobrenosotros():
    return render_template('Sitio/sobrenosotros.html')

@app.route('/formulario')
def formulario():
    return render_template('Sitio/formulario.html')

@app.route('/procesar_formulario', methods=['POST'])
def procesar_formulario():
    _nombre = request.form['nombre']
    _telefono = request.form['telefono']
    _ciudad = request.form['ciudad']
    _correo = request.form['correo']
    _mensaje = request.form['mensaje']

    sql = """INSERT INTO `paginawebwm` (`Nombre`, `Telefono`, `Ciudad`, `Correo`, `Mensaje`, `Fecha`)
             VALUES (%s, %s, %s, %s, %s, NOW());"""
    paginawebwm = (_nombre, _telefono, _ciudad, _correo, _mensaje)

    conexion = None  # Inicializar la variable antes del bloque try

    try:
        # Intentar conectar a la base de datos
        conexion = mysql.connector.connect(**db_config)
        
        if conexion.is_connected():
            cursor = conexion.cursor()
            cursor.execute(sql, paginawebwm)
            conexion.commit()
            flash('Formulario procesado correctamente.', 'success')  # Mensaje de éxito
        else:
            flash('No se pudo conectar a la base de datos.', 'error')

    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        flash(f'Error al conectar a la base de datos: {e}', 'error')  # Mensaje de error

    finally:
        if conexion is not None and conexion.is_connected():
            conexion.close()

    # Mostrar datos en consola (solo para pruebas)
    print(_nombre, _telefono, _ciudad, _correo, _mensaje)

    return render_template('Sitio/formulario.html')

if __name__ == '__main__':
    app.run(debug=True)

