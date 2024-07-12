from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

app = Flask(__name__)

# Configuración de la base de datos MySQL para SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Definición de los modelos
class Registracion(db.Model):
    __tablename__ = 'registracion'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)

class Reserva(db.Model):
    __tablename__ = 'reserva'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre_dueño = db.Column(db.String(100), nullable=False)
    nombre_mascota = db.Column(db.String(100), nullable=False)
    fecha_turno = db.Column(db.Date, nullable=False)

# Rutas de la aplicación
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registro', methods=['POST'])
def registro():
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({"message": "El email es requerido"}), 400

    try:
        # Verifica si el email ya existe
        if Registracion.query.filter_by(email=email).first():
            return jsonify({"message": "El email ya está registrado"}), 400

        nuevo_usuario = Registracion(email=email)
        db.session.add(nuevo_usuario)
        db.session.commit()
        return jsonify({"message": "Registro exitoso"})
    except Exception as e:
        print(f"Error en el registro de usuario: {e}")
        db.session.rollback()
        return jsonify({"message": "Error en el registro"}), 500

@app.route('/turno', methods=['POST'])
def turno():
    data = request.get_json()
    nombre_dueño = data.get('nombre_dueño')
    nombre_mascota = data.get('nombre_mascota')
    fecha_turno_str = data.get('fecha_turno')

    if not all([nombre_dueño, nombre_mascota, fecha_turno_str]):
        return jsonify({"message": "Todos los campos son requeridos"}), 400

    try:
        from datetime import datetime
        try:
            fecha_turno = datetime.strptime(fecha_turno_str, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({"message": "Fecha en formato incorrecto, debe ser YYYY-MM-DD"}), 400
        
        nuevo_turno = Reserva(nombre_dueño=nombre_dueño, nombre_mascota=nombre_mascota, fecha_turno=fecha_turno)
        db.session.add(nuevo_turno)
        db.session.commit()
        return jsonify({"message": "Turno registrado exitosamente"})
    except Exception as e:
        print(f"Error en el registro del turno: {e}")
        db.session.rollback()
        return jsonify({"message": "Error en el registro del turno"}), 500

@app.route('/turnos', methods=['GET'])
def obtener_turnos():
    turnos = Reserva.query.all()
    return jsonify([{
        'id': t.id,
        'nombre_dueño': t.nombre_dueño,
        'nombre_mascota': t.nombre_mascota,
        'fecha_turno': t.fecha_turno.strftime('%Y-%m-%d')
    } for t in turnos])

@app.route('/turno/<int:id>', methods=['GET'])
def obtener_turno(id):
    turno = Reserva.query.get(id)
    if turno:
        return jsonify({
            'id': turno.id,
            'nombre_dueño': turno.nombre_dueño,
            'nombre_mascota': turno.nombre_mascota,
            'fecha_turno': turno.fecha_turno.strftime('%Y-%m-%d')
        })
    return jsonify({"message": "Turno no encontrado"}), 404

@app.route('/turno/<int:id>', methods=['PUT'])
def actualizar_turno(id):
    data = request.get_json()
    turno = Reserva.query.get(id)

    if not turno:
        return jsonify({"message": "Turno no encontrado"}), 404

    nombre_dueño = data.get('nombre_dueño')
    nombre_mascota = data.get('nombre_mascota')
    fecha_turno_str = data.get('fecha_turno')

    if not all([nombre_dueño, nombre_mascota, fecha_turno_str]):
        return jsonify({"message": "Todos los campos son requeridos"}), 400

    try:
        from datetime import datetime
        try:
            fecha_turno = datetime.strptime(fecha_turno_str, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({"message": "Fecha en formato incorrecto, debe ser YYYY-MM-DD"}), 400

        turno.nombre_dueño = nombre_dueño
        turno.nombre_mascota = nombre_mascota
        turno.fecha_turno = fecha_turno

        db.session.commit()
        return jsonify({"message": "Turno actualizado exitosamente"})
    except Exception as e:
        print(f"Error en la actualización del turno: {e}")
        db.session.rollback()
        return jsonify({"message": "Error en la actualización del turno"}), 500

@app.route('/turno/<int:id>', methods=['DELETE'])
def eliminar_turno(id):
    turno = Reserva.query.get(id)

    if not turno:
        return jsonify({"message": "Turno no encontrado"}), 404

    try:
        db.session.delete(turno)
        db.session.commit()
        return jsonify({"message": "Turno eliminado exitosamente"})
    except Exception as e:
        print(f"Error en la eliminación del turno: {e}")
        db.session.rollback()
        return jsonify({"message": "Error en la eliminación del turno"}), 500

if __name__ == '__main__':
    app.run(debug=True)
