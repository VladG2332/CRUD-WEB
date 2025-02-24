from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuración de PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://root:te9GmgGXIUlsC0vyP8Mx55o1VYbFIe0d@dpg-cups6bdsvqrc73f5b4gg-a.oregon-postgres.render.com/cetech_oj50'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo
class Estudiante(db.Model):
    __tablename__ = 'alumnos'
    no_control = db.Column(db.String(10), primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    ap_paterno = db.Column(db.String(100), nullable=False)
    ap_materno = db.Column(db.String(100), nullable=False)
    semestre = db.Column(db.Integer, nullable=False)

# Crear tablas
with app.app_context():
    db.create_all()

# Ruta para listar estudiantes
@app.route('/estudiantes', methods=['GET'])
def obtener_estudiantes():
    estudiantes = Estudiante.query.all()
    return jsonify([{
        'no_control': e.no_control, 'nombre': e.nombre,
        'ap_paterno': e.ap_paterno, 'ap_materno': e.ap_materno, 'semestre': e.semestre
    } for e in estudiantes])

# Ruta para agregar estudiante
@app.route('/nuevo_estudiante')
def nuevo_estudiante():
    return render_template('nuevo_estudiante.html')

@app.route('/agregar_estudiante', methods=['POST'])
def agregar_estudiante():
    data = request.get_json()
    nuevo_estudiante = Estudiante(
        no_control=data['no_control'],
        nombre=data['nombre'],
        ap_paterno=data['ap_paterno'],
        ap_materno=data['ap_materno'],
        semestre=data['semestre']
    )
    db.session.add(nuevo_estudiante)
    db.session.commit()
    return jsonify({'mensaje': 'Estudiante agregado con éxito'})

# Ruta para eliminar estudiante
@app.route('/eliminar_estudiante/<no_control>', methods=['DELETE'])
def eliminar_estudiante(no_control):
    estudiante = Estudiante.query.filter_by(no_control=no_control).first()
    if estudiante:
        db.session.delete(estudiante)
        db.session.commit()
        return jsonify({'mensaje': 'Estudiante eliminado'})
    return jsonify({'mensaje': 'Estudiante no encontrado'}), 404

# Ruta para editar estudiante
@app.route('/editar_estudiante/<no_control>', methods=['GET'])
def editar_estudiante(no_control):
    estudiante = Estudiante.query.filter_by(no_control=no_control).first()
    if estudiante:
        return render_template('editar_estudiante.html', estudiante=estudiante)
    return jsonify({'mensaje': 'Estudiante no encontrado'}), 404

@app.route('/actualizar_estudiante', methods=['POST'])
def actualizar_estudiante():
    data = request.get_json()
    estudiante = Estudiante.query.filter_by(no_control=data['no_control']).first()
    if estudiante:
        estudiante.nombre = data['nombre']
        estudiante.ap_paterno = data['ap_paterno']
        estudiante.ap_materno = data['ap_materno']
        estudiante.semestre = data['semestre']
        db.session.commit()
        return jsonify({'mensaje': 'Estudiante actualizado'})
    return jsonify({'mensaje': 'Estudiante no encontrado'}), 404

@app.route('/obtener_estudiante/<no_control>', methods=['GET'])
def obtener_estudiante(no_control):
    estudiante = Estudiante.query.filter_by(no_control=no_control).first()
    if estudiante:
        return jsonify({
            'no_control': estudiante.no_control,
            'nombre': estudiante.nombre,
            'ap_paterno': estudiante.ap_paterno,
            'ap_materno': estudiante.ap_materno,
            'semestre': estudiante.semestre
        })
    return jsonify({'mensaje': 'Estudiante no encontrado'}), 404

# Ruta principal
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)