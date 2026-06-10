# Medicare+ — Full Stack Healthcare Platform
## Flask Backend + HTML/CSS/JS Frontend

---

## 🚀 Quick Start

### 1. Backend (Flask)
```bash
cd backend
pip install -r requirements.txt
python app.py
```
Flask runs on → http://localhost:5000
Database auto-creates with seed data (doctors + patient accounts).

### 2. Frontend
Open `frontend/index.html` in your browser.
Or serve with:
```bash
cd frontend
python -m http.server 3000
```
Then visit → http://localhost:3000

---

## 🔑 Demo Accounts
| Role    | Email                    | Password    |
|---------|--------------------------|-------------|
| Patient | patient@medicare.com     | patient123  |
| Doctor  | priya@medicare.com       | doctor123   |
| Doctor  | arjun@medicare.com       | doctor123   |

---

## 📁 Project Structure
```
medicare-plus/
├── backend/
│   ├── app.py              ← Flask app entry point
│   ├── database.py         ← SQLAlchemy instance
│   ├── models.py           ← All DB models
│   ├── requirements.txt
│   └── routes/
│       ├── auth.py         ← Login / Register
│       ├── appointments.py ← Booking + slots
│       ├── prescriptions.py
│       ├── doctors.py
│       ├── symptoms.py     ← Symptom checker logic
│       ├── chat.py         ← Messaging
│       ├── reports.py      ← File upload
│       ├── reminders.py
│       ├── reviews.py
│       └── emergency.py
│
└── frontend/
    ├── index.html          ← Login / Register
    ├── dashboard.html      ← Health overview
    ├── appointments.html   ← Book & manage
    ├── doctors.html        ← Search & filter
    ├── prescriptions.html  ← View & create
    ├── symptoms.html       ← AI checker
    ├── chat.html           ← Messaging
    ├── reports.html        ← Upload files
    ├── reminders.html      ← Medicine alerts
    ├── emergency.html      ← SOS + contacts
    ├── shared.css          ← Design system
    └── shared.js           ← API helpers + sidebar
```

---

## ✅ Features Implemented
1. 📅 Smart Appointment Booking — slot availability, double-booking prevention
2. 💊 Prescription Generator — doctor creates, patient views & prints
3. 🤖 Symptom Checker — select symptoms → diseases + specialist suggestions
4. 🚨 Emergency Help — SOS button, ambulance/hospital contacts, first aid
5. 📋 Patient Health Dashboard — stats, upcoming appointments, reminders
6. ⏰ Medicine Reminders — add/pause/delete, time + frequency
7. 💬 Doctor–Patient Chat — real-time polling, conversation list
8. 📄 Medical Report Upload — PDF/image upload, view & delete
9. 🔍 Smart Doctor Search — filter by specialty, fees, experience
10. ⭐ Ratings & Reviews — 1–5 stars, comments, average shown on cards

---

## 🛠 Tech Stack
- **Backend**: Python Flask, SQLAlchemy, Flask-JWT-Extended, Flask-CORS
- **Database**: SQLite (file: backend/medicare.db)
- **Frontend**: Pure HTML + CSS + Vanilla JavaScript
- **Auth**: JWT tokens stored in localStorage
