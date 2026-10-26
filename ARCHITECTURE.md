# MediCare — Application Architecture

## 1. Overview

MediCare is a full-stack medical appointment portal demonstrating authentication, role-based access control, relational database design, appointment management, and automated testing.

The application combines a React and TypeScript frontend with a Flask backend and PostgreSQL database.

> **Note:** All appointment records in this project are demo/test data, not real appointments.

## 2. Technology Stack

| Layer | Technology |
|---|---|
| Frontend | React, TypeScript, Vite |
| HTTP client | Axios |
| Backend | Python, Flask |
| Authentication | Flask-Login, Werkzeug password hashing |
| ORM | Flask-SQLAlchemy, SQLAlchemy |
| Database | PostgreSQL |
| Database driver | Psycopg |
| Security | Flask-WTF CSRF protection |
| Testing | pytest |

## 3. High-Level Architecture

The application follows a client-server architecture.

```text
User
 |
 v
React + TypeScript
 |
 | HTTP requests through Axios
 | Session cookies and CSRF token
 v
Flask Application
 |
 +--> Authentication and authorisation
 |
 +--> Appointment management
 |
 +--> Patient profiles
 |
 +--> Doctor management
 |
 v
SQLAlchemy ORM
 |
 v
PostgreSQL Database
```

The React frontend communicates with Flask through HTTP requests. Flask handles authentication, authorisation, validation, business logic, and database operations.

The application also retains Flask-rendered pages for existing portal functionality.

## 4. Frontend

The frontend uses React, TypeScript, and Vite. Axios handles HTTP requests to the Flask backend.

The Axios configuration includes credentials so browser requests can carry session cookies.

### Login Flow

1. The user enters an email address and password.
2. The frontend requests a CSRF token from Flask.
3. Axios submits the credentials with the `X-CSRFToken` header.
4. Flask validates the credentials and establishes an authenticated session.
5. The frontend redirects the user to the existing Flask booking page.

The frontend is integrated with the Flask application; the entire user interface has not yet been migrated to React.

## 5. Backend

Flask handles API requests, server-rendered pages, authentication, authorisation, and application logic.

Its responsibilities include:

- Authenticating users.
- Protecting routes that require login.
- Restricting administrative functionality by role.
- Checking patient profiles before booking.
- Creating and retrieving appointments.
- Managing doctor records.
- Updating appointment statuses.
- Returning API responses and rendering HTML templates.

## 6. Database Design

PostgreSQL stores the application's relational data. SQLAlchemy models represent the main entities.

### Users

The `users` table stores:

- `id` — primary key.
- `email` — required email address.
- `password_hash` — hashed password.
- `role` — patient or administrator.
- `created_at` — account creation timestamp.

A case-insensitive unique index on `LOWER(email)` prevents duplicate email addresses that differ only in capitalisation.

A check constraint restricts roles to `patient` and `admin`.

### Patients

The `patients` table stores patient profile information, including:

- Patient ID and associated user ID.
- Full name and email.
- Date of birth and address.
- Blood type.
- GP name and contact details.
- Creation timestamp.

The user ID links a patient profile to a user account.

### Doctors

The `doctors` table stores doctor information, including:

- Doctor ID, full name, and email.
- Speciality, qualifications, and biography.
- Hospital, station, and department.
- Salary and availability.
- Creation timestamp.

The email column is required and unique.

### Bookings

The `bookings` table stores:

- Booking ID.
- Patient ID, where associated.
- Patient name and email.
- Doctor.
- Appointment date and time.
- Appointment status.

Appointment statuses supported by the application include `Confirmed`, `Cancelled`, and `Completed`.

## 7. Authentication and Authorisation

Flask-Login manages authenticated user sessions.

The application supports two roles:

- **Patient:** Can access patient-specific functionality, including their profile and appointment history.
- **Administrator:** Can access protected administrative functionality, including doctor management and appointment administration.

Protected routes require authentication. Administrative routes additionally verify that the current user has the administrator role.

Passwords are hashed before storage using Werkzeug rather than being stored as plain text.

## 8. Appointment Booking Flow

The booking process follows these steps:

1. The user signs in.
2. The user opens the booking page.
3. Flask checks whether the patient has a profile.
4. The request supplies the doctor, date, and time.
5. The backend checks whether the doctor already has a booking for that time slot.
6. If a conflict is detected, the booking is rejected.
7. Otherwise, the booking is saved to PostgreSQL with a `Confirmed` status.
8. The application returns a response or displays a message.

The shared `add_booking()` function performs the application-level conflict check and saves the booking.

Database-level protection against simultaneous conflicting bookings should be considered as a further improvement.

## 9. Security

The application implements several security measures:

- Password hashing using Werkzeug.
- Session-based authentication with Flask-Login.
- Role-based protection for administrative routes.
- Login-required protection for private pages and API endpoints.
- CSRF protection using Flask-WTF.
- CSRF token transmission from the React frontend through the `X-CSRFToken` header.
- Parameterised SQL in the direct Psycopg user-creation function.
- Environment variables for database connection settings.

For production deployment, additional configuration should include HTTPS, secure session-cookie settings, restricted database permissions, and protected secret management.

## 10. Testing

The project uses pytest to test application behaviour.

Tests should cover authentication, access restrictions, booking creation, booking conflicts, patient record access, administrator operations, and error handling.

Tests should use suitable test configuration and test data rather than relying on production records.

## 11. Potential Improvements

Future improvements include:

- Migrating more of the interface to React.
- Adding database-level protection against conflicting appointment slots.
- Managing schema changes with database migrations.
- Strengthening appointment date and time validation.
- Expanding automated tests for authentication and booking edge cases.
- Improving API error handling and frontend loading states.
- Configuring production-grade HTTPS, cookies, and secret management.

## 12. Project Status

MediCare demonstrates a full-stack application integrating React, Flask, PostgreSQL, authentication, role-based access, patient profiles, doctor management, appointment booking, and automated testing.

This document describes the current architecture and should be updated as the application evolves.
