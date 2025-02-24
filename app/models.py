from . import db

class Estudiante(db.Model):
    __tablename__ = 'alumnos'
    no_control = db.Column(db.String(10), primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    ap_paterno = db.Column(db.String(100), nullable=False)
    ap_materno = db.Column(db.String(100), nullable=False)
    semestre = db.Column(db.Integer, nullable=False)