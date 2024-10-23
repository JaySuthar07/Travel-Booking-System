
# Travel Booking System - README

This document provides instructions to set up and use the Travel Booking System, as well as an overview of the main features implemented.

---

## Table of Contents

1. System Requirements
2. Installation Instructions
3. Setting Up the Database
4. Starting the Application
5. Implemented Features
6. How to Use the System

---

## 1. System Requirements

- **Ubuntu (20.04 or newer)**
- **Python 3.8 or newer**
- **Flask**
- **PostgreSQL or SQLite (for database)**
- **pip (Python package installer)**

---

## 2. Installation Instructions

Follow these steps to set up the system:

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

## 3. Setting Up the Database

1. **Initialize the database**:
   Run the following commands to set up the database tables and models:
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

2. **Configure environment variables**:
   Set up your `.env` file with the required configurations for database connection (PostgreSQL or SQLite).

   Example for PostgreSQL:
   ```
   DATABASE_URL=postgresql://user:password@localhost:5432/travel_booking
   ```

---

## 4. Starting the Application

To start the Flask development server, run:
```bash
flask run
```

The application will now be running at `http://127.0.0.1:5000/`.

---

## 5. Implemented Features

- **User Registration and Login**: Users can sign up and log in.
- **Flight and Hotel Booking**: Users can book flights and hotels independently.
- **Package Deals**: Users can book a combined package (flight + hotel) at a discounted price.
- **Booking Cancellation**: Users can cancel their bookings (flights, hotels, or packages).
- **Admin Dashboard**: Admins can view and manage all user bookings and reservations.
- **Availability Updates**: The system updates the availability of flights and hotels based on bookings and cancellations.
- **Dynamic Pricing**: Package deals automatically calculate the total price based on selected flights and hotels.

---

## 6. How to Use the System

1. **User Registration**:
   - Navigate to the registration page.
   - Fill in the username, email, and password to create an account.

2. **Login**:
   - Enter your registered email and password on the login page to access your dashboard.

3. **Booking a Flight or Hotel**:
   - Go to the booking section.
   - Select a flight or hotel, and specify travel dates.

4. **Booking a Package**:
   - Choose from available package deals.
   - Review flight and hotel details, and confirm your booking.

5. **Cancelling a Booking**:
   - On your dashboard, you can view your bookings.
   - Click on "Cancel" to cancel any confirmed booking.

6. **Admin Features**:
   - Admin users can view and manage all bookings.
   - Admins can see the total price of packages and individual bookings.

---

This should help you get the Travel Booking System up and running. If you have any questions, feel free to ask!
