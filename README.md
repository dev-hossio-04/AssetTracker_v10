# Asset Tracker System

Offline Flask-based Asset Management System built with Python, Flask, and SQLite.

---

# Overview

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

# Features

## Asset Management
- Add new assets
- Edit assets
- Asset categorization
- Asset status tracking
- Flexible asset ID system

## Asset Status Support
- Available
- Checked Out
- Returned
- Under Repair
- Damaged
- Lost
- Retired
- Permanently Assigned

## User Management
- Admin accounts
- Staff accounts
- Viewer accounts
- Password authentication
- Password reset support

## Transaction Tracking
- Check-in
- Check-out
- Authorized by tracking
- Performed by tracking
- PC hostname tracking
- Audit logs

## Reporting
- Dashboard overview
- Recent activity
- Excel export
- Transaction history

## Flexible Assignment System
- Manual assignment support
- Optional staff database
- Optional staff ID
- Supports:
  - staff
  - freelancers
  - vendors
  - temporary crews
  - organizations

## Database
- SQLite local database
- Portable
- Easy backup
- Offline support

---

# Technology Stack

| Component | Technology |
|---|---|
| Backend | Flask |
| Database | SQLite |
| Frontend | HTML / CSS |
| ORM | SQLAlchemy |
| Authentication | Flask-Login |
| Excel Export | OpenPyXL |

---

# Requirements

- Python 3.11+
- Windows / Linux
- Modern web browser

---

# Installation Guide

## 1. Clone Repository

```bash
git clone https://github.com/dev-hossio-04/AssetTracker_v10
```

---

## 2. Open Project Folder

```bash
cd AssetTracker_v10
```

---

## 3. Create Virtual Environment

```bash
python -m venv .venv
```

---

## 4. Activate Virtual Environment

### Windows PowerShell

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
```

### Windows CMD

```cmd
.venv\Scripts\activate.bat
```

---

## 5. Install Required Packages

```bash
python -m pip install -r requirements.txt
```

---

## 6. Run System

```bash
python run.py
```

---

## 7. Open Browser

```text
http://127.0.0.1:5000
```

---

# Default Login

| Username | Password |
|---|---|
| admin | admin123 |

IMPORTANT:
Change the default password immediately after first login.

---

# Easier Deployment Method (Recommended)

The project includes:

```text
start_asset_tracker.bat
stop_asset_tracker.bat
```

## Start System

Simply double-click:

```text
start_asset_tracker.bat
```

This will:
- activate Python environment
- start Flask server
- launch system locally

---

## Stop System

Double-click:

```text
stop_asset_tracker.bat
```

This will safely stop the Asset Tracker server.

---

# Accessing From Other PCs (LAN)

Edit `run.py`:

```python
app.run(debug=False, host="0.0.0.0", port=5000)
```

Find your IP address:

```bash
ipconfig
```

Example:

```text
192.xxx.x.xx
```

Other devices on the same network can access:

```text
http://192.xxx.x.xx:5000
```

---

# Asset ID Prefix System

| Asset Type | Prefix |
|---|---|
| Laptop | NCSM |
| Printer | PRI |
| Presenter | PRE |
| Pendrive | PEN |
| Power Adapter | ADC |
| Monitor | MON |
| Keyboard | KEY |
| Mouse | MOU |
| Headset | HPE |
| Camera | CAM |
| Router | ROU |
| Switch | SWI |


# Project Structure

```text
AssetTracker_v10/
│
├── app/
├── database/
│   └── assets.db
│
├── exports/
├── reports/
├── backups/
│
├── run.py
├── requirements.txt
├── start_asset_tracker.bat
├── stop_asset_tracker.bat
│
├── LICENSE
├── README.md
└── VERSION
```

---

# Database Backup

IMPORTANT:

Backup this file regularly:

```text
database/assets.db
```

This file contains:
- assets
- users
- transactions
- audit logs

---

# Deployment To PC

## 1. Install Python

Download:
https://www.python.org/downloads/

IMPORTANT:
Enable:

```text
Add Python to PATH
```

---

## 2. Open Project Folder

```bash
cd AssetTracker_v10
```

---

## 3. Create Virtual Environment

```bash
python -m venv .venv
```

---

## 4. Activate Virtual Environment

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
```

---

## 5. Install Packages

```bash
python -m pip install -r requirements.txt
```

---

## 6. Start System

Double-click:

```text
start_asset_tracker.bat
```

---

# Security Notes

Recommended:
- Use strong passwords
- Backup database regularly
- Do not expose directly to the internet
- Disable debug mode in production

---

# License

This project is licensed under the MIT License.

You are free to:
- use
- modify
- distribute
- publish
- improve

with proper license inclusion.

See `LICENSE` file for details.

---

# Disclaimer

This software is provided "AS IS", without warranty of any kind.

Users are responsible for:
- securing their deployment
- managing backups
- protecting organizational data

---

# Credits

Developed by ElanDev

Built with:
- Flask
- SQLite
- SQLAlchemy
- OpenPyXL

---



# Community Contributions

Community improvements, suggestions, and pull requests are welcome.

---

# Version

Current Version:

```text
v1.0.0
```
