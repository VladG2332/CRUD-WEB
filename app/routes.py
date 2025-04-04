from flask import Blueprint, jsonify, render_template, request
from .models import Estudiante
from . import db

# Crear un Blueprint para las rutas
estudiantes_bp = Blueprint('estudiantes', __name__)

@estudiantes_bp.route('/estudiantes', methods=['GET'])
def obtener_estudiantes():
    estudiantes = Estudiante.query.all()
    return jsonify([{
        'no_control': e.no_control, 'nombre': e.nombre,
        'ap_paterno': e.ap_paterno, 'ap_materno': e.ap_materno, 'semestre': e.semestre
    } for e in estudiantes])

@estudiantes_bp.route('/nuevo_estudiante')
def nuevo_estudiante():
    return render_template('nuevo_estudiante.html')

@estudiantes_bp.route('/agregar_estudiante', methods=['POST'])
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

@estudiantes_bp.route('/eliminar_estudiante/<no_control>', methods=['DELETE'])
def eliminar_estudiante(no_control):
    estudiante = Estudiante.query.filter_by(no_control=no_control).first()
    if estudiante:
        db.session.delete(estudiante)
        db.session.commit()
        return jsonify({'mensaje': 'Estudiante eliminado'})
    return jsonify({'mensaje': 'Estudiante no encontrado'}), 404

@estudiantes_bp.route('/editar_estudiante/<no_control>', methods=['GET'])
def editar_estudiante(no_control):
    estudiante = Estudiante.query.filter_by(no_control=no_control).first()
    if estudiante:
        return render_template('editar_estudiante.html', estudiante=estudiante)
    return jsonify({'mensaje': 'Estudiante no encontrado'}), 404

@estudiantes_bp.route('/actualizar_estudiante', methods=['POST'])
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

@estudiantes_bp.route('/obtener_estudiante/<no_control>', methods=['GET'])
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

@estudiantes_bp.route('/')
def index():
    return render_template('index.html')