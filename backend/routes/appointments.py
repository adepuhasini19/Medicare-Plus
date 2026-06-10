from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from database import db
from models import Appointment, Doctor, User

appointments_bp = Blueprint('appointments', __name__)

@appointments_bp.route('/', methods=['GET'])
@jwt_required()
def get_appointments():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if user.role == 'patient':
        appts = Appointment.query.filter_by(patient_id=user_id).order_by(Appointment.date.desc()).all()
    else:
        doctor = Doctor.query.filter_by(user_id=user_id).first()
        appts = Appointment.query.filter_by(doctor_id=doctor.id).order_by(Appointment.date.desc()).all() if doctor else []
    return jsonify([a.to_dict() for a in appts])

@appointments_bp.route('/', methods=['POST'])
@jwt_required()
def book_appointment():
    user_id = int(get_jwt_identity())
    data = request.get_json()
    doctor_id = data['doctor_id']
    date = data['date']
    time = data['time']
    # Check double booking
    existing = Appointment.query.filter_by(doctor_id=doctor_id, date=date, time=time).filter(
        Appointment.status.in_(['pending', 'confirmed'])
    ).first()
    if existing:
        return jsonify({'error': 'This slot is already booked. Please choose another time.'}), 409
    appt = Appointment(
        patient_id=user_id, doctor_id=doctor_id,
        date=date, time=time, reason=data.get('reason', ''),
        status='pending'
    )
    db.session.add(appt)
    db.session.commit()
    return jsonify(appt.to_dict()), 201

@appointments_bp.route('/<int:appt_id>', methods=['PUT'])
@jwt_required()
def update_appointment(appt_id):
    user_id = int(get_jwt_identity())
    appt = Appointment.query.get_or_404(appt_id)
    data = request.get_json()
    appt.status = data.get('status', appt.status)
    db.session.commit()
    return jsonify(appt.to_dict())

@appointments_bp.route('/slots', methods=['GET'])
@jwt_required()
def get_available_slots():
    doctor_id = request.args.get('doctor_id')
    date = request.args.get('date')
    all_slots = ['09:00', '09:30', '10:00', '10:30', '11:00', '11:30', '14:00', '14:30', '15:00', '15:30', '16:00', '16:30']
    booked = Appointment.query.filter_by(doctor_id=doctor_id, date=date).filter(
        Appointment.status.in_(['pending', 'confirmed'])
    ).all()
    booked_times = [a.time for a in booked]
    available = [s for s in all_slots if s not in booked_times]
    return jsonify({'slots': available, 'booked': booked_times})
