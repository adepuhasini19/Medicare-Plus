from flask import Blueprint, request, jsonify, send_from_directory, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from database import db
from models import MedicalReport
from werkzeug.utils import secure_filename
import os, time

reports_bp = Blueprint('reports', __name__)
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@reports_bp.route('/', methods=['GET'])
@jwt_required()
def get_reports():
    user_id = int(get_jwt_identity())
    reports = MedicalReport.query.filter_by(patient_id=user_id).order_by(MedicalReport.created_at.desc()).all()
    return jsonify([r.to_dict() for r in reports])

@reports_bp.route('/', methods=['POST'])
@jwt_required()
def upload_report():
    user_id = int(get_jwt_identity())
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    file = request.files['file']
    if not file or not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type'}), 400
    filename = secure_filename(file.filename)
    unique_name = f"{user_id}_{int(time.time())}_{filename}"
    file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], unique_name))
    report = MedicalReport(
        patient_id=user_id, title=request.form.get('title', filename),
        filename=unique_name, file_type=filename.rsplit('.', 1)[1].lower(),
        report_date=request.form.get('report_date', '')
    )
    db.session.add(report)
    db.session.commit()
    return jsonify(report.to_dict()), 201

@reports_bp.route('/file/<filename>', methods=['GET'])
@jwt_required()
def get_report_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)

@reports_bp.route('/<int:report_id>', methods=['DELETE'])
@jwt_required()
def delete_report(report_id):
    user_id = int(get_jwt_identity())
    report = MedicalReport.query.get_or_404(report_id)
    if report.patient_id != user_id:
        return jsonify({'error': 'Forbidden'}), 403
    db.session.delete(report)
    db.session.commit()
    return jsonify({'message': 'Deleted'})
