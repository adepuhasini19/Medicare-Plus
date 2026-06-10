from database import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='patient')  # patient, doctor
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    doctor_profile = db.relationship('Doctor', backref='user', uselist=False)
    appointments_as_patient = db.relationship('Appointment', foreign_keys='Appointment.patient_id', backref='patient')
    sent_messages = db.relationship('Message', foreign_keys='Message.sender_id', backref='sender')

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'email': self.email, 'role': self.role, 'phone': self.phone}

class Doctor(db.Model):
    __tablename__ = 'doctors'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    specialty = db.Column(db.String(100))
    fees = db.Column(db.Float, default=0)
    experience = db.Column(db.Integer, default=0)
    available_days = db.Column(db.String(100), default='Mon,Tue,Wed,Thu,Fri')
    bio = db.Column(db.Text)
    rating_sum = db.Column(db.Float, default=0)
    rating_count = db.Column(db.Integer, default=0)

    def avg_rating(self):
        if self.rating_count == 0:
            return 0
        return round(self.rating_sum / self.rating_count, 1)

    def to_dict(self):
        return {
            'id': self.id, 'user_id': self.user_id,
            'name': self.user.name, 'email': self.user.email,
            'specialty': self.specialty, 'fees': self.fees,
            'experience': self.experience, 'bio': self.bio,
            'available_days': self.available_days,
            'avg_rating': self.avg_rating(), 'rating_count': self.rating_count
        }

class Appointment(db.Model):
    __tablename__ = 'appointments'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    time = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, confirmed, cancelled, completed
    reason = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    doctor = db.relationship('Doctor', backref='appointments')

    def to_dict(self):
        return {
            'id': self.id, 'patient_id': self.patient_id,
            'doctor_id': self.doctor_id, 'doctor_name': self.doctor.user.name,
            'specialty': self.doctor.specialty,
            'date': self.date, 'time': self.time,
            'status': self.status, 'reason': self.reason,
            'created_at': self.created_at.isoformat()
        }

class Prescription(db.Model):
    __tablename__ = 'prescriptions'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.id'), nullable=True)
    diagnosis = db.Column(db.Text)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    medicines = db.relationship('PrescriptionMedicine', backref='prescription', cascade='all, delete-orphan')
    doctor = db.relationship('Doctor')
    patient = db.relationship('User', foreign_keys=[patient_id])

    def to_dict(self):
        return {
            'id': self.id, 'patient_id': self.patient_id,
            'doctor_id': self.doctor_id, 'doctor_name': self.doctor.user.name,
            'patient_name': self.patient.name,
            'diagnosis': self.diagnosis, 'notes': self.notes,
            'medicines': [m.to_dict() for m in self.medicines],
            'created_at': self.created_at.isoformat()
        }

class PrescriptionMedicine(db.Model):
    __tablename__ = 'prescription_medicines'
    id = db.Column(db.Integer, primary_key=True)
    prescription_id = db.Column(db.Integer, db.ForeignKey('prescriptions.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    dosage = db.Column(db.String(100))
    frequency = db.Column(db.String(100))
    duration = db.Column(db.String(50))
    instructions = db.Column(db.Text)

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'dosage': self.dosage,
                'frequency': self.frequency, 'duration': self.duration, 'instructions': self.instructions}

class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    receiver = db.relationship('User', foreign_keys=[receiver_id])

    def to_dict(self):
        return {
            'id': self.id, 'sender_id': self.sender_id, 'receiver_id': self.receiver_id,
            'sender_name': self.sender.name, 'content': self.content,
            'is_read': self.is_read, 'created_at': self.created_at.isoformat()
        }

class MedicalReport(db.Model):
    __tablename__ = 'medical_reports'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(50))
    report_date = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    patient = db.relationship('User', foreign_keys=[patient_id])

    def to_dict(self):
        return {
            'id': self.id, 'patient_id': self.patient_id,
            'title': self.title, 'filename': self.filename,
            'file_type': self.file_type, 'report_date': self.report_date,
            'created_at': self.created_at.isoformat()
        }

class MedicineReminder(db.Model):
    __tablename__ = 'medicine_reminders'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    medicine_name = db.Column(db.String(100), nullable=False)
    dosage = db.Column(db.String(100))
    reminder_time = db.Column(db.String(10), nullable=False)
    frequency = db.Column(db.String(50), default='daily')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id, 'medicine_name': self.medicine_name,
            'dosage': self.dosage, 'reminder_time': self.reminder_time,
            'frequency': self.frequency, 'is_active': self.is_active
        }

class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    patient = db.relationship('User', foreign_keys=[patient_id])
    doctor = db.relationship('Doctor', foreign_keys=[doctor_id])

    def to_dict(self):
        return {
            'id': self.id, 'patient_name': self.patient.name,
            'doctor_id': self.doctor_id, 'rating': self.rating,
            'comment': self.comment, 'created_at': self.created_at.isoformat()
        }

class EmergencyContact(db.Model):
    __tablename__ = 'emergency_contacts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    number = db.Column(db.String(20), nullable=False)
    contact_type = db.Column(db.String(30), default='ambulance')

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'number': self.number, 'contact_type': self.contact_type}
