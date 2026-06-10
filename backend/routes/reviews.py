from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from database import db
from models import Review, Doctor

reviews_bp = Blueprint('reviews', __name__)

@reviews_bp.route('/<int:doctor_id>', methods=['GET'])
@jwt_required()
def get_doctor_reviews(doctor_id):
    reviews = Review.query.filter_by(doctor_id=doctor_id).order_by(Review.created_at.desc()).all()
    return jsonify([r.to_dict() for r in reviews])

@reviews_bp.route('/', methods=['POST'])
@jwt_required()
def create_review():
    user_id = int(get_jwt_identity())
    data = request.get_json()
    doctor_id = data['doctor_id']
    existing = Review.query.filter_by(patient_id=user_id, doctor_id=doctor_id).first()
    if existing:
        old_rating = existing.rating
        existing.rating = data['rating']
        existing.comment = data.get('comment', '')
        doctor = Doctor.query.get(doctor_id)
        doctor.rating_sum = doctor.rating_sum - old_rating + data['rating']
        db.session.commit()
        return jsonify(existing.to_dict())
    review = Review(patient_id=user_id, doctor_id=doctor_id, rating=data['rating'], comment=data.get('comment', ''))
    db.session.add(review)
    doctor = Doctor.query.get(doctor_id)
    doctor.rating_sum += data['rating']
    doctor.rating_count += 1
    db.session.commit()
    return jsonify(review.to_dict()), 201
