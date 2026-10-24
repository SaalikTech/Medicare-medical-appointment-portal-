# MediCare — Medical Appointment Portal

## Project Overview
A full-stack healthcare appointment management application built with Flask, React, TypeScript and PostgreSQL.

The MediCare Medical Appointment Portal helps patients book appointments with doctors, view their medical profile and appiontment history, while allowing administrators to manage doctors, patient profiles, and appointment records.

The system includes booking conflict checks to help prevent double-booking and supports appointment management through a user-friendly interface. 

It uses Flask for the backend, React and TypeScript for the frontend, and PostgreSQL for data storage, providing a structured and secure foundation for managing medical appointments.

---

## Features
**Patient**
- **Register and login** securely.
- Manage **patient profile** information.
- **View available doctors** 
- **Book** medical appointments.
- ***View appointment** history and **booking status**.

**Administrator**
- **Access a protected** admin dashboard.
- **Add and manage** doctor records.
- **View and manage** appointments.
- **Update** appointment statuses.
- **Export appointment** data

**Security**
- Password hashing.
- Role-based access control for patients and administrators.
- Login-protected routes.
- CSRF protection for supported Flask form submissions.
- Session cookie security settings.
- Environment variables for database configuration and credentials.
---

## Dependencies
### Backend
- **Flask** — web framework and API.
- **Flask-SQLAlchemy & SQLAlchemy** — database integration and ORM.
- **PostgreSQL & Psycopg** — relational data storage and database connectivity.
- **Flask-Login** — authentication and session management.
- **Flask-WTF** — CSRF protection.
- **Flask-CORS** — cross-origin API requests.
- **python-dotenv** — environment configuration.
- **Pytest** — automated testing.
### Frontend Dependencies

- **React** — builds the user interface.
- **React DOM** — renders React components in the browser.
- **TypeScript** — provides static typing.
- **Vite** — frontend development server and production build tool.
- **Axios** — communicates with the Flask backend API.
- **Oxlint** — checks code for potential issues.
- **Node.js and npm** — run the development tools and manage packages.

Frontend dependencies are managed through `frontend/package.json`, with exact resolved versions recorded in `frontend/package-lock.json`.

---

## ▶️ How to Run the Application

### Prerequisites
- Python
- Node.js and npm
- PostgreSQL

### 1. Start the Backend
From the project root, activate the Python virtual environment:
**Windows PowerShell**

.\venv\Scripts\Activate.ps1

Install the backend dependencies:

pip install -r requirements.txt

Configure PostgreSQL connection & environment variables as required by the application.

Start the Flask server:
python app.py

Backend: `http://127.0.0.1:5000`

### 2. Start the Frontend

Open a **second terminal** and navigate to the frontend directory:

cd frontend

Install the frontend dependencies:

npm install

Start the React development server:
npm run dev

Frontend: `http://localhost:5173`

Open the frontend URL displayed by Vite in your browser.

### 3. Run the Tests

From the project root, with the Python virtual environment activated:
pytest -v

### 4. Build the Frontend for Production

From the `frontend` directory:
npm run build

The production-ready frontend files are generated in the `frontend/dist` directory.

**Note:** Keep the Flask backend and React development server running in separate terminals while using the application. Ensure PostgreSQL is running and the database connection is configured correctly.

http://127.0.0.1:5000/      -> Booking page
http://127.0.0.1:5000/admin -> Admin panel
http://127.0.0.1:5000/export_json -> Export all bookings as JSON



