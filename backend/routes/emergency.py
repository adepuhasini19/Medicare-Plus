from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from models import EmergencyContact

emergency_bp = Blueprint('emergency', __name__)

@emergency_bp.route('/', methods=['GET'])
@jwt_required()
def get_emergency_contacts():
    contacts = EmergencyContact.query.all()
    return jsonify([c.to_dict() for c in contacts])
