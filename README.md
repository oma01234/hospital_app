## 🏥 Hospital Management System
A full-stack hospital management platform built with Django that serves patients, medical staff, and administrators through both web interfaces and REST APIs.

## 🚀 Overview
This project is a comprehensive hospital management system designed to digitize and streamline healthcare operations.

**It solves problems like:**
- Fragmented patient records
- Manual appointment scheduling
- Poor communication between staff and patients
- Lack of real-time monitoring and reporting
- Complex billing and insurance workflows

**The system is built for:**
- Hospitals (private and general)
- Clinics
- Medical centers
- Healthcare startups

I built this to create a scalable, API-ready healthcare platform that supports both web-based usage and future mobile app integration.


## 🛠 Tech Stack
- Backend: Python, Django
- API: Django REST Framework
- Database: PostgreSQL / SQLite
- Frontend: HTML, CSS (Django Templates)
- Authentication: Django Auth + Role-Based Access Control
- Tools: Docker, Celery (for background tasks), Postman

## ⚙️ Key Features
**👤 Patient-Centric Features**
- Patient registration and profile management
- Online appointment booking
- Virtual consultations (text/video ready)
- Electronic Medical Records (EMR) access
- Prescription viewing and renewals
- Medication and treatment reminders
- Health vitals tracking
- Billing and online payments
- Insurance claim tracking
- Emergency request system


**🩺 Medical Staff-Centric Features**
- Staff registration and authentication
- Role-based access (Doctor, Nurse, Admin)
- Doctor schedule management
- Automated appointment assignment
- Consultation notes and patient history
- Care plan creation and monitoring
- EHR updates and lab result management
- Electronic prescription management
- Internal messaging and collaboration
- Clinical decision support (drug interaction checker, guidelines)
- Emergency alerts and code activation
- Inventory and supply management

## 🔐 Security & Access Control
- Role-based permissions
- Authenticated API endpoints
- Protected patient data access
- Separation between staff and patient privileges

## 🧠 Architecture / Design Decisions
**Why Django?**
Django was chosen because it provides:
- Built-in authentication
- Admin panel for hospital administrators
- Strong ORM for relational data modeling
- Security features out of the box
- Scalability for enterprise-level systems

**Why Separate Template Views and API Views?**
The system is structured with:
- views.py → Template-based frontend views
- api_views.py → RESTful API endpoints

This allows:
- Web application usage via templates
- Mobile app integration via API
- Clear separation of concerns
- Easier future scaling

## Role-Based Access Design
- Staff roles are implemented using Django Groups and permissions.
- Doctors, nurses, and admins have controlled access to features.
- Patients cannot access staff-only data.
- API endpoints enforce IsAuthenticated and custom role permissions.

## Background Tasks
- Celery can be integrated for:
- Appointment reminders
- Medication alerts
- Emergency notifications
- Insurance processing

## 📡 API Endpoints

**Authentication**
| Method | Endpoint                  | Description      |
| ------ | ------------------------- | ---------------- |
| POST   | `/patients/api/register/` | Register patient |
| POST   | `/staff/api/register/`    | Register staff   |
| GET    | `/patients/api/profile/`  | Get profile      |


**Appointments**
| Method | Endpoint                          | Description        |
| ------ | --------------------------------- | ------------------ |
| GET    | `/appointments/api/appointments/` | List appointments  |
| POST   | `/appointments/api/appointments/` | Create appointment |
| GET    | `/appointments/api/doctors/`      | List doctors       |

**Medical Records**
| Method | Endpoint                      | Description              |
| ------ | ----------------------------- | ------------------------ |
| GET    | `/medical/api/records/`       | Retrieve medical records |
| POST   | `/medical/api/prescriptions/` | Create prescription      |
| GET    | `/medical/api/labs/`          | View lab results         |


**Billing & Insurance**
| Method | Endpoint                         | Description            |
| ------ | -------------------------------- | ---------------------- |
| GET    | `/patients/api/bills/`           | View bills             |
| POST   | `/patients/api/insurance/claim/` | Submit insurance claim |

**Messaging**
| Method | Endpoint                       | Description    |
| ------ | ------------------------------ | -------------- |
| GET    | `/communication/api/messages/` | Fetch messages |
| POST   | `/communication/api/messages/` | Send message   |


## 🗄 Database Design
**Core Models:**
- User (Django default)
- Doctor (OneToOne → User)
- Patient Profile (OneToOne → User)
- Appointment (ForeignKey → Patient, Doctor)
- MedicalRecord (ForeignKey → Patient)
- Prescription (ForeignKey → Patient, Doctor)
- TreatmentPlan
- VitalSigns
- Bill
- InsuranceClaim
- InventoryItem

**Relationships**
- One doctor → many appointments
- One patient → many medical records
- Many staff members → many messages
- One patient → many prescriptions

ForeignKey and OneToOne relationships are used extensively to maintain relational integrity.

## 🧪 How to Run Locally
- git clone https://github.com/oma01234/hospital_app
- cd hospital-management-system
- python -m venv venv
- source venv/bin/activate  # or venv\Scripts\activate on Windows
- pip install -r requirements.txt
- python manage.py migrate
- python manage.py createsuperuser
- python manage.py runserver

## 📌 Future Improvements
- Full WebSocket real-time chat
- Payment gateway integration (Stripe/Paystack)
- AI-powered diagnostic support
- Mobile app integration
- Advanced reporting dashboard
- Multi-hospital (multi-tenant) architecture

