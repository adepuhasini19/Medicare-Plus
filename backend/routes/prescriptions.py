from flask import Blueprint, request, jsonify, send_from_directory, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from database import db
from models import Prescription, PrescriptionMedicine, Doctor, User
import json

prescriptions_bp = Blueprint('prescriptions', __name__)

@prescriptions_bp.route('/', methods=['GET'])
@jwt_required()
def get_prescriptions():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if user.role == 'patient':
        prescs = Prescription.query.filter_by(patient_id=user_id).order_by(Prescription.created_at.desc()).all()
    else:
        doctor = Doctor.query.filter_by(user_id=user_id).first()
        prescs = Prescription.query.filter_by(doctor_id=doctor.id).order_by(Prescription.created_at.desc()).all() if doctor else []
    return jsonify([p.to_dict() for p in prescs])

@prescriptions_bp.route('/', methods=['POST'])
@jwt_required()
def create_prescription():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if user.role != 'doctor':
        return jsonify({'error': 'Only doctors can create prescriptions'}), 403
    doctor = Doctor.query.filter_by(user_id=user_id).first()
    data = request.get_json()
    presc = Prescription(
        patient_id=data['patient_id'], doctor_id=doctor.id,
        diagnosis=data.get('diagnosis', ''), notes=data.get('notes', '')
    )
    db.session.add(presc)
    db.session.flush()
    for med in data.get('medicines', []):
        m = PrescriptionMedicine(
            prescription_id=presc.id, name=med['name'],
            dosage=med.get('dosage', ''), frequency=med.get('frequency', ''),
            duration=med.get('duration', ''), instructions=med.get('instructions', '')
        )
        db.session.add(m)
    db.session.commit()
    return jsonify(presc.to_dict()), 201

@prescriptions_bp.route('/<int:presc_id>/pdf', methods=['GET'])
@jwt_required()
def download_prescription_pdf(presc_id):
    presc = Prescription.query.get_or_404(presc_id)
    # Return prescription data for client-side PDF generation
    return jsonify(presc.to_dict())
