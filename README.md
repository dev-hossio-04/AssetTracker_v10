# Asset Tracker System

Offline Flask-based Asset Management System built with Python, Flask, and SQLite.

---

## Overview

Asset Tracker System is a lightweight offline asset management solution designed for:

- IT departments
- event teams
- schools
- organizations
- small businesses
- community projects

The system supports:

- asset inventory management
- check-in / check-out tracking
- audit logging
- multiple user logins
- reporting
- Excel export
- offline local deployment

Built for simplicity, flexibility, and future scalability.

---

## Features

### Asset Management

- Add new assets
- Edit assets
- Asset categorization
- Asset status tracking
- Flexible asset ID system

### Asset Status Support

- Available
- Checked Out
- Returned
- Under Repair
- Damaged
- Lost
- Retired
- Permanently Assigned

### User Management

- Admin accounts
- Staff accounts
- Viewer accounts
- Password authentication
- Password reset support

### Transaction Tracking

- Check-in
- Check-out
- Authorized by tracking
- Performed by tracking
- PC hostname tracking
- Audit logs

### Reporting

- Dashboard overview
- Recent activity
- Excel export
- Transaction history

### Flexible Assignment System

- Manual assignment support
- Optional staff database
- Optional staff ID

Supports:

- staff
- freelancers
- vendors
- temporary crews
- organizations

### Database

- SQLite local database
- Portable
- Easy backup
- Offline support

---

## Technology Stack

| Component | Technology |
|---|---|
| Backend | Flask |
| Database | SQLite |
| Frontend | HTML / CSS |
| ORM | SQLAlchemy |
| Authentication | Flask-Login |
| Excel Export | OpenPyXL |

---

## Requirements

- Python 3.11+
- Windows / Linux
- Modern web browser

---

## Installation

### 1. Clone or Download Project

```bash
git clone https://github.com/dev-hossio-04/AssetTracker_v10



2. Open Project Folder
cd AssetTracker_v10

3. Create Virtual Environment
python -m venv .venv
4. Activate Virtual Environment
Windows PowerShell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
Windows CMD
.venv\Scripts\activate.bat
5. Install Requirements
python -m pip install -r requirements.txt

If pip is not recognized, use:

python -m pip install flask flask-login flask-sqlalchemy werkzeug openpyxl
6. Create Database
python create_db.py
7. Create Default Admin / Sample Data
python seed_data.py
8. Run System Manually
python run.py

Then open:

http://127.0.0.1:5000
Default Login
Username	Password
admin	admin123

Important: change the default admin password after first login.

Easier Start / Stop Method

After setup is complete, you can start and stop the system using batch files.

Start System

Double-click:

start_asset_tracker.bat

Or run:

start_asset_tracker.bat
Stop System

Double-click:

stop_asset_tracker.bat

Or run:

stop_asset_tracker.bat

The stop script stops the service running on port 5000.
