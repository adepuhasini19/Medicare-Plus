from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

symptoms_bp = Blueprint('symptoms', __name__)

SYMPTOM_DB = {
    'fever': {'diseases': ['Flu', 'Malaria', 'COVID-19', 'Typhoid'], 'doctor': 'General Physician'},
    'headache': {'diseases': ['Migraine', 'Tension Headache', 'Hypertension'], 'doctor': 'Neurologist'},
    'chest_pain': {'diseases': ['Angina', 'Heart Attack', 'GERD'], 'doctor': 'Cardiologist'},
    'cough': {'diseases': ['Common Cold', 'Bronchitis', 'Pneumonia', 'COVID-19'], 'doctor': 'General Physician'},
    'fatigue': {'diseases': ['Anemia', 'Diabetes', 'Thyroid disorder', 'Depression'], 'doctor': 'General Physician'},
    'joint_pain': {'diseases': ['Arthritis', 'Gout', 'Rheumatoid Arthritis'], 'doctor': 'Orthopedist'},
    'skin_rash': {'diseases': ['Eczema', 'Psoriasis', 'Allergic Reaction'], 'doctor': 'Dermatologist'},
    'stomach_pain': {'diseases': ['Gastritis', 'Appendicitis', 'IBS', 'Ulcer'], 'doctor': 'General Physician'},
    'dizziness': {'diseases': ['Vertigo', 'Low Blood Pressure', 'Inner ear disorder'], 'doctor': 'Neurologist'},
    'shortness_of_breath': {'diseases': ['Asthma', 'Pneumonia', 'Heart Failure'], 'doctor': 'Cardiologist'},
    'anxiety': {'diseases': ['Anxiety Disorder', 'Panic Disorder', 'Depression'], 'doctor': 'Psychiatrist'},
    'nausea': {'diseases': ['Food Poisoning', 'Gastroenteritis', 'Pregnancy'], 'doctor': 'General Physician'},
}

ALL_SYMPTOMS = [
    {'id': k, 'label': k.replace('_', ' ').title()} for k in SYMPTOM_DB.keys()
]

@symptoms_bp.route('/list', methods=['GET'])
@jwt_required()
def list_symptoms():
    return jsonify(ALL_SYMPTOMS)

@symptoms_bp.route('/check', methods=['POST'])
@jwt_required()
def check_symptoms():
    data = request.get_json()
    selected = data.get('symptoms', [])
    if not selected:
        return jsonify({'error': 'No symptoms provided'}), 400
    
    diseases = []
    doctors = set()
    for s in selected:
        if s in SYMPTOM_DB:
            diseases.extend(SYMPTOM_DB[s]['diseases'])
            doctors.add(SYMPTOM_DB[s]['doctor'])
    
    from collections import Counter
    disease_counts = Counter(diseases)
    top_diseases = [{'name': d, 'likelihood': min(int(c * 30), 95)} 
                    for d, c in disease_counts.most_common(4)]
    
    severity = 'low'
    if 'chest_pain' in selected or 'shortness_of_breath' in selected:
        severity = 'high'
    elif len(selected) >= 3:
        severity = 'medium'
    
    return jsonify({
        'possible_diseases': top_diseases,
        'suggested_doctors': list(doctors),
        'severity': severity,
        'disclaimer': 'This is not a medical diagnosis. Please consult a qualified doctor.'
    })
