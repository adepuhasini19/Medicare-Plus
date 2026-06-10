from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from database import db
from models import Doctor, User

doctors_bp = Blueprint('doctors', __name__)

@doctors_bp.route('/', methods=['GET'])
@jwt_required()
def get_doctors():
    specialty = request.args.get('specialty', '')
    max_fees = request.args.get('max_fees', type=float)
    min_exp = request.args.get('min_exp', type=int)
    
    query = Doctor.query
    if specialty:
        query = query.filter(Doctor.specialty.ilike(f'%{specialty}%'))
    if max_fees:
        query = query.filter(Doctor.fees <= max_fees)
    if min_exp:
        query = query.filter(Doctor.experience >= min_exp)
    
    doctors = query.all()
    return jsonify([d.to_dict() for d in doctors])

@doctors_bp.route('/<int:doctor_id>', methods=['GET'])
@jwt_required()
def get_doctor(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    return jsonify(doctor.to_dict())

@doctors_bp.route('/specialties', methods=['GET'])
@jwt_required()
def get_specialties():
    from sqlalchemy import distinct
    specialties = db.session.query(distinct(Doctor.specialty)).all()
    return jsonify([s[0] for s in specialties])

@doctors_bp.route('/patients', methods=['GET'])
@jwt_required()
def get_doctor_patients():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if user.role != 'doctor':
        return jsonify({'error': 'Forbidden'}), 403
    doctor = Doctor.query.filter_by(user_id=user_id).first()
    from models import Appointment
    patient_ids = db.session.query(Appointment.patient_id).filter_by(doctor_id=doctor.id).distinct().all()
    patients = User.query.filter(User.id.in_([p[0] for p in patient_ids])).all()
    return jsonify([p.to_dict() for p in patients])
