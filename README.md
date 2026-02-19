# 🎬 ClapLog — Professional Film Production Tracker

<div align="center">

![ClapLog Logo](streamlit_app/assets/Logo.png)

**A full-stack film production management system built with Django + Streamlit**

[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)](https://python.org)
[![Django](https://img.shields.io/badge/Django-5.0.1-green?logo=django)](https://djangoproject.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.x-red?logo=streamlit)](https://streamlit.io)
[![MySQL](https://img.shields.io/badge/MySQL-8.0+-orange?logo=mysql)](https://mysql.com)
[![License](https://img.shields.io/badge/License-MIT-purple)](LICENSE)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Running the App](#-running-the-app)
- [API Reference](#-api-reference)
- [Pages Guide](#-pages-guide)
- [Database Schema](#-database-schema)
- [Contributing](#-contributing)

---

## 🎯 Overview

ClapLog is a comprehensive film production tracking application that helps directors, producers, and crew members manage every aspect of their production — from initial scene planning to final shot completion.

Built with a **Django REST API backend** and a **Streamlit frontend**, it features real-time production statistics, call sheet management, continuity tracking, cast & props management, and more.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🎬 **Productions** | Create and manage multiple productions with status tracking |
| 📋 **Scenes** | Track scenes with status, location, cast requirements |
| 📷 **Shots** | Detailed shot management with camera specs |
| 📅 **Call Sheets** | Generate and manage daily call sheets |
| 🎭 **Cast Members** | Cast database with character assignments |
| 🪄 **Props** | Props inventory tracking per scene |
| 🔄 **Continuity** | Continuity notes and issue tracking |
| 📊 **Dashboard** | Live stats: completion %, scene counts, shot counts |
| 🔐 **Auth** | JWT authentication with email verification |
| 🌊 **Deep Ocean Theme** | Professional dark UI with cyan accents |

---

## 🛠 Tech Stack

**Backend**
- Python 3.10+
- Django 5.0.1
- Django REST Framework
- SimpleJWT (authentication)
- MySQL 8.0+
- django-filter
- django-cors-headers

**Frontend**
- Streamlit
- Custom CSS (Deep Ocean Professional theme)
- Google Fonts (Tangerine, Dancing Script, Inter)
- Base64 image embedding

**Email**
- Gmail SMTP with App Passwords
- JWT-based email verification

---

## 📁 Project Structure

```
ClapLog/
│
├── claplog/                    # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── api_urls.py             # API router
│
├── apps/                       # Django applications
│   ├── users/                  # User auth & profiles
│   ├── productions/            # Productions CRUD
│   ├── scenes/                 # Scenes management
│   ├── shots/                  # Shot tracking
│   ├── call_sheets/            # Call sheet generation
│   ├── cast/                   # Cast members
│   ├── props/                  # Props inventory
│   └── continuity/             # Continuity notes
│
├── streamlit_app/              # Streamlit frontend
│   ├── app.py                  # Main entry point (login + dashboard)
│   ├── pages/                  # Streamlit pages
│   │   ├── Productions.py
│   │   ├── Scenes.py
│   │   ├── Shots.py
│   │   ├── Call_Sheets.py
│   │   ├── Cast_Members.py
│   │   ├── Props.py
│   │   └── Continuity.py
│   ├── api/
│   │   └── client.py           # API client (all HTTP calls)
│   ├── components/
│   │   ├── logo.py             # Logo display component
│   │   ├── visuals.py          # Film quotes, dividers
│   │   ├── animations.py       # Success animations
│   │   └── production_selector.py
│   └── styles/
│       └── dark_theme.py       # Deep Ocean CSS theme
│
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## ⚙️ Installation

### Prerequisites

- Python 3.10+
- MySQL 8.0+
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/ClapLog.git
cd ClapLog
```

### 2. Create Virtual Environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up MySQL Database

```sql
CREATE DATABASE claplog CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'claplog_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON claplog.* TO 'claplog_user'@'localhost';
FLUSH PRIVILEGES;
```

### 5. Configure Environment

```bash
cp .env.example .env
# Edit .env with your values (see Configuration section)
```

### 6. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Create Superuser (optional)

```bash
python manage.py createsuperuser
```

---

## 🔧 Configuration

Create a `.env` file in the project root:

```env
# Django
SECRET_KEY=your-very-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=claplog
DB_USER=claplog_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=3306

# Email (Gmail SMTP)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your.email@gmail.com
EMAIL_HOST_PASSWORD=your-gmail-app-password
EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL=ClapLog <your.email@gmail.com>

# JWT
JWT_SECRET_KEY=your-jwt-secret
JWT_EXPIRY_HOURS=24

# Frontend URL (for email verification links)
FRONTEND_URL=http://localhost:8501
```

> **Gmail App Password:** Go to Google Account → Security → 2-Step Verification → App Passwords → Generate for "Mail"

---

## 🚀 Running the App

You need **two terminals** running simultaneously:

### Terminal 1 — Django Backend

```bash
# Activate venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # macOS/Linux

# Start Django
python manage.py runserver
# Runs at: http://127.0.0.1:8000
```

### Terminal 2 — Streamlit Frontend

```bash
# Activate venv
.venv\Scripts\activate  # Windows

# Start Streamlit
cd streamlit_app
streamlit run app.py
# Runs at: http://localhost:8501
```

### Access the App

| Service | URL |
|---|---|
| Streamlit App | http://localhost:8501 |
| Django Admin | http://localhost:8000/admin |
| API Root | http://localhost:8000/api/ |
| Network (LAN) | http://YOUR_IP:8501 |

---

## 📡 API Reference

All endpoints require `Authorization: Bearer <token>` header except `/api/auth/`.

### Authentication

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/auth/register/` | Register new user |
| POST | `/api/auth/login/` | Login, returns JWT token |
| GET | `/api/auth/verify-email/?token=` | Verify email address |
| POST | `/api/auth/resend-verification/` | Resend verification email |
| GET | `/api/auth/me/` | Get current user info |

### Productions

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/productions/` | List all productions |
| POST | `/api/productions/` | Create production |
| GET | `/api/productions/{id}/` | Get single production |
| PATCH | `/api/productions/{id}/` | Update production |
| DELETE | `/api/productions/{id}/` | Delete production |
| GET | `/api/productions/{id}/statistics/` | Live stats (scenes, shots, %) |
| PATCH | `/api/productions/{id}/update_status/` | Quick status update |

### Scenes

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/scenes/?production={id}` | List scenes for production |
| POST | `/api/scenes/` | Create scene |
| PATCH | `/api/scenes/{id}/` | Update scene (status, notes, etc.) |
| DELETE | `/api/scenes/{id}/` | Delete scene |

### Shots

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/shots/?scene={id}` | List shots for scene |
| POST | `/api/shots/` | Create shot |
| PATCH | `/api/shots/{id}/` | Update shot |
| DELETE | `/api/shots/{id}/` | Delete shot |

### Other Endpoints

```
/api/call-sheets/
/api/cast-members/
/api/props/
/api/continuity-notes/
```

---

## 📱 Pages Guide

### 🏠 Dashboard (`app.py`)
- Live production stats (total scenes, shots, completion %)
- Production cards with real progress bars
- Quick action buttons
- Production summary table

### 🎬 Productions (`pages/Productions.py`)
- Create new productions with title, description, dates, status
- Update production status (Development → Pre-Production → Filming → Post → Completed)
- View all productions with scene/shot counts

### 📋 Scenes (`pages/Scenes.py`)
- Add scenes to a production
- Update scene status: `not_started → in_progress → completed → on_hold`
- Marking scenes as **completed** updates the dashboard completion %

### 📷 Shots (`pages/Shots.py`)
- Add shots to scenes
- Track: shot type, camera angle, lens, aperture, ISO, frame rate
- VFX requirements flag

### 📅 Call Sheets (`pages/Call_Sheets.py`)
- Create daily call sheets
- Set call times, locations, scenes for the day
- Cast requirements per call sheet

### 🎭 Cast Members (`pages/Cast_Members.py`)
- Cast database management
- Character assignments to productions

### 🪄 Props (`pages/Props.py`)
- Props inventory per production
- Scene-level prop assignments

### 🔄 Continuity (`pages/Continuity.py`)
- Log continuity issues per scene
- Categories: costume, makeup, props, lighting, etc.
- Severity: low, medium, high, critical
- Status: open, in_progress, resolved

---

## 🗄 Database Schema

```
productions          scenes              shots
─────────────        ──────────────      ──────────────
id                   id                  id
title                production (FK)     scene (FK)
description          scene_number        shot_number
status               title               shot_type
start_date           description         camera_angle
end_date             location            camera_movement
created_by (FK)      status              lens
created_at           cast_required       aperture
                     day_night           iso
                     interior_exterior   frame_rate
                                         take_count

call_sheets          cast_members        props
────────────         ─────────────       ──────────
id                   id                  id
production (FK)      production (FK)     production (FK)
date                 actor_name          name
call_time            character_name      description
location             role_type           scene (FK)
scenes               contact             quantity
notes                availability        status

continuity_notes
────────────────
id
scene (FK)
category
severity
status
description
actor_character
```

---

## 🔄 Scene Status Flow

```
not_started  →  in_progress  →  completed
                    ↓
                 on_hold
```

Updating a scene to `completed` automatically updates:
- Dashboard completion percentage
- Production progress bars
- "At a Glance" stats panel

---

## 🌱 .gitignore

Make sure your `.gitignore` includes:

```gitignore
# Python
.venv/
__pycache__/
*.pyc
*.pyo
*.pyd
.Python

# Environment
.env
*.env

# Django
db.sqlite3
*.log
media/

# Streamlit
.streamlit/secrets.toml

# IDE
.idea/
.vscode/
*.swp

# OS
.DS_Store
Thumbs.db
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit changes: `git commit -m "Add: your feature description"`
4. Push: `git push origin feature/your-feature`
5. Open a Pull Request

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

<div align="center">
Built with ❤️ for filmmakers everywhere 🎬
</div>
