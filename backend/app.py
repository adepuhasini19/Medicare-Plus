from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from database import db
from routes.auth import auth_bp
from routes.appointments import appointments_bp
from routes.prescriptions import prescriptions_bp
from routes.symptoms import symptoms_bp
from routes.doctors import doctors_bp
from routes.chat import chat_bp
from routes.reports import reports_bp
from routes.reminders import reminders_bp
from routes.reviews import reviews_bp
from routes.emergency import emergency_bp
import os


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///medicare.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'medicare-plus-secret-key-2024'
    app.config['UPLOAD_FOLDER'] = 'uploads'
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Allow requests from any origin (good for demo/portfolio)
    CORS(app)

    JWTManager(app)
    db.init_app(app)

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(appointments_bp, url_prefix='/api/appointments')
    app.register_blueprint(prescriptions_bp, url_prefix='/api/prescriptions')
    app.register_blueprint(symptoms_bp, url_prefix='/api/symptoms')
    app.register_blueprint(doctors_bp, url_prefix='/api/doctors')
    app.register_blueprint(chat_bp, url_prefix='/api/chat')
    app.register_blueprint(reports_bp, url_prefix='/api/reports')
    app.register_blueprint(reminders_bp, url_prefix='/api/reminders')
    app.register_blueprint(reviews_bp, url_prefix='/api/reviews')
    app.register_blueprint(emergency_bp, url_prefix='/api/emergency')

    with app.app_context():
        db.create_all()
        seed_data()

    return app


def seed_data():
    from models import User, Doctor, EmergencyContact
    from werkzeug.security import generate_password_hash

    if User.query.first():
        return

    doctors_data = [
        {'name': 'Dr. Priya Sharma', 'specialty': 'Cardiologist', 'fees': 800, 'experience': 12, 'email': 'priya@medicare.com', 'phone': '040-2345-6789'},
        {'name': 'Dr. Arjun Reddy', 'specialty': 'Neurologist', 'fees': 1000, 'experience': 15, 'email': 'arjun@medicare.com', 'phone': '040-3456-7890'},
        {'name': 'Dr. Meera Nair', 'specialty': 'Pediatrician', 'fees': 500, 'experience': 8, 'email': 'meera@medicare.com', 'phone': '040-4567-8901'},
        {'name': 'Dr. Vikram Patel', 'specialty': 'Orthopedist', 'fees': 700, 'experience': 10, 'email': 'vikram@medicare.com', 'phone': '040-5678-9012'},
        {'name': 'Dr. Ananya Iyer', 'specialty': 'Dermatologist', 'fees': 600, 'experience': 7, 'email': 'ananya@medicare.com', 'phone': '040-6789-0123'},
        {'name': 'Dr. Ravi Kumar', 'specialty': 'General Physician', 'fees': 400, 'experience': 20, 'email': 'ravi@medicare.com', 'phone': '040-7890-1234'},
        {'name': 'Dr. Sunita Rao', 'specialty': 'Gynecologist', 'fees': 750, 'experience': 14, 'email': 'sunita@medicare.com', 'phone': '040-8901-2345'},
        {'name': 'Dr. Karan Mehta', 'specialty': 'Psychiatrist', 'fees': 900, 'experience': 9, 'email': 'karan@medicare.com', 'phone': '040-9012-3456'},
    ]

    for d in doctors_data:
        user = User(
            name=d['name'],
            email=d['email'],
            password=generate_password_hash('doctor123'),
            role='doctor',
            phone=d['phone']
        )
        db.session.add(user)
        db.session.flush()

        doctor = Doctor(
            user_id=user.id,
            specialty=d['specialty'],
            fees=d['fees'],
            experience=d['experience'],
            available_days='Mon,Tue,Wed,Thu,Fri',
            bio=f"Experienced {d['specialty']} with {d['experience']} years of practice."
        )

        db.session.add(doctor)

    patient = User(
        name='Rahul Verma',
        email='patient@medicare.com',
        password=generate_password_hash('patient123'),
        role='patient',
        phone='9876543210'
    )

    db.session.add(patient)

    emergencies = [
        {'name': 'Hyderabad Emergency', 'number': '108', 'type': 'ambulance'},
        {'name': 'KIMS Hospital', 'number': '040-44885000', 'type': 'hospital'},
        {'name': 'Apollo Hospital', 'number': '040-23607777', 'type': 'hospital'},
        {'name': 'Police', 'number': '100', 'type': 'police'},
        {'name': 'Fire', 'number': '101', 'type': 'fire'},
    ]

    for e in emergencies:
        ec = EmergencyContact(
            name=e['name'],
            number=e['number'],
            contact_type=e['type']
        )
        db.session.add(ec)

    db.session.commit()


# Create app instance for Gunicorn
app = create_app()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)