from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from database import db
from models import MedicineReminder

reminders_bp = Blueprint('reminders', __name__)

@reminders_bp.route('/', methods=['GET'])
@jwt_required()
def get_reminders():
    user_id = int(get_jwt_identity())
    reminders = MedicineReminder.query.filter_by(patient_id=user_id).all()
    return jsonify([r.to_dict() for r in reminders])

@reminders_bp.route('/', methods=['POST'])
@jwt_required()
def create_reminder():
    user_id = int(get_jwt_identity())
    data = request.get_json()
    reminder = MedicineReminder(
        patient_id=user_id, medicine_name=data['medicine_name'],
        dosage=data.get('dosage', ''), reminder_time=data['reminder_time'],
        frequency=data.get('frequency', 'daily')
    )
    db.session.add(reminder)
    db.session.commit()
    return jsonify(reminder.to_dict()), 201

@reminders_bp.route('/<int:rem_id>', methods=['DELETE'])
@jwt_required()
def delete_reminder(rem_id):
    user_id = int(get_jwt_identity())
    reminder = MedicineReminder.query.get_or_404(rem_id)
    if reminder.patient_id != user_id:
        return jsonify({'error': 'Forbidden'}), 403
    db.session.delete(reminder)
    db.session.commit()
    return jsonify({'message': 'Deleted'})

@reminders_bp.route('/<int:rem_id>/toggle', methods=['PUT'])
@jwt_required()
def toggle_reminder(rem_id):
    reminder = MedicineReminder.query.get_or_404(rem_id)
    reminder.is_active = not reminder.is_active
    db.session.commit()
    return jsonify(reminder.to_dict())
