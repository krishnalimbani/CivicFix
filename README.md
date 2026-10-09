# 🏙️ CivicFix — Smart Civic Issue Reporting System

> **IBM / BCA Final Year Project | IBM | UN SDG 11 — Sustainable Cities and Communities**

CivicFix is a full-stack web application that enables citizens to report and track civic issues such as potholes, broken streetlights, garbage overflow, and drainage problems. It connects citizens to local authorities with a real-time reporting dashboard and interactive map.

---

## 📸 Features

| Feature | Description |
|---|---|
| 🏠 **Homepage** | Hero section, statistics counters, issue categories, recent reports |
| 📝 **Report Issue** | Form with category selector, description, map pin, photo upload |
| 🔍 **Track Report** | Look up any report by unique ID with visual status timeline |
| 🗺️ **Live Map** | Leaflet.js map showing all geo-tagged reports with status filters |
| 🆔 **Unique IDs** | Auto-generated Report IDs (e.g., `CF-A1B2C3D4`) for tracking |
| 🔐 **Admin Panel** | Secure login, full dashboard, status updates, delete reports |
| 📊 **API Endpoints** | `/api/reports` and `/api/stats` for JSON data |
| 📱 **Responsive** | Works on desktop, tablet, and mobile |

---

## 🛠️ Tech Stack

- **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5, Bootstrap Icons
- **Backend:** Python Flask
- **Database:** SQLite (file-based, no setup needed)
- **Maps:** Leaflet.js + OpenStreetMap (free, no API key)
- **Fonts:** Google Fonts (Inter, Poppins)

---

## 📂 Project Structure

```
CivicFix/
├── app.py                    # Main Flask application
├── database.py               # DB init, connection, seed data
├── civicfix.db               # SQLite database (auto-created)
├── requirements.txt          # Python dependencies
│
├── templates/
│   ├── base.html             # Base layout (navbar, footer)
│   ├── index.html            # Homepage
│   ├── report.html           # Report Issue form
│   ├── track.html            # Track Report page
│   ├── map.html              # Interactive Map page
│   ├── admin_login.html      # Admin Login
│   ├── admin_dashboard.html  # Admin Dashboard
│   └── admin_report_detail.html  # Single report view
│
└── static/
    ├── css/style.css         # All styles + animations
    ├── js/main.js            # Scroll animations, counters
    └── uploads/              # Uploaded photos stored here
```

---

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.8 or newer
- pip (comes with Python)

### Step 1 — Clone / Download the project

Place the `CivicFix` folder anywhere on your computer.

### Step 2 — Open Terminal / Command Prompt

Navigate to the project folder:
```bash
cd path\to\CivicFix
```

### Step 3 — Install Dependencies

```bash
pip install flask werkzeug
```

### Step 4 — Run the Application

```bash
python app.py
```

You should see:
```
* Running on http://127.0.0.1:5000
```

### Step 5 — Open in Browser

Visit: **http://127.0.0.1:5000**

---

## 🔐 Admin Panel

| URL | http://127.0.0.1:5000/admin/login |
|---|---|
| **Username** | `admin` |
| **Password** | `civicfix@admin` |

The admin can:
- View all submitted reports
- Filter by status or category
- Search by keyword / location / ID
- Update report status (Submitted → Under Review → In Progress → Resolved)
- View full report detail including photo and map
- Delete reports

---

## 📡 API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/api/reports` | GET | Returns all geo-tagged reports as JSON |
| `/api/stats` | GET | Returns summary statistics as JSON |

---

## 🗺️ Report Status Flow

```
Submitted → Under Review → In Progress → Resolved
```

---

## 📦 Requirements File

```
flask
werkzeug
```

Create `requirements.txt` (already provided) and install with:
```bash
pip install -r requirements.txt
```

---

## 🌍 UN SDG Alignment

This project directly supports **UN Sustainable Development Goal 11: Sustainable Cities and Communities** by:
- Empowering citizens to participate in urban governance
- Enabling transparent tracking of civic issue resolution
- Creating data-driven visibility for local authorities
- Promoting accountability in public infrastructure maintenance

---

## 👨‍💻 Built By

**Krishna Limbani**  
BCA Student | IBM SkillsBuild Project  
CivicFix © 2024
