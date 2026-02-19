# 🚀 ClapLog Deployment Guide

## Option 1: Railway (Recommended - Free Tier)

Railway provides free hosting for both Django backend and PostgreSQL database.

### Prerequisites
- GitHub account with ClapLog repository
- Railway account (sign up at railway.app)

### Step-by-Step Deployment

#### 1. Add Deployment Files to Your Repo

Add these files to your project root:
- `railway.json` (Railway configuration)
- `nixpacks.toml` (Build configuration)
- `requirements-deploy.txt` (Production dependencies)

Then update `claplog/settings.py` for production:

```python
# At the top, add:
import dj_database_url
import os

# Update ALLOWED_HOSTS
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# Update DATABASES for Railway (uses PostgreSQL, not MySQL)
DATABASES = {
    'default': dj_database_url.config(
        default=f"mysql://{os.getenv('DB_USER', 'root')}:{os.getenv('DB_PASSWORD', '')}@{os.getenv('DB_HOST', 'localhost')}:{os.getenv('DB_PORT', '3306')}/{os.getenv('DB_NAME', 'claplog')}",
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# Add whitenoise to MIDDLEWARE (after SecurityMiddleware)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # ← Add this
    # ... rest of middleware
]

# Static files for production
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Security settings for production
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
```

#### 2. Deploy Django Backend on Railway

1. Go to https://railway.app
2. Click "New Project" → "Deploy from GitHub repo"
3. Select `mudita15sharma/ClapLog`
4. Railway will auto-detect Django and start building

#### 3. Add Database

1. In your Railway project, click "New" → "Database" → "PostgreSQL"
2. Railway automatically creates a PostgreSQL database
3. Environment variable `DATABASE_URL` is auto-added

#### 4. Set Environment Variables

In Railway dashboard, go to your service → "Variables" → Add:

```
SECRET_KEY=your-production-secret-key-here
DEBUG=False
ALLOWED_HOSTS=claplog-production.up.railway.app
EMAIL_HOST_USER=your.email@gmail.com
EMAIL_HOST_PASSWORD=your-gmail-app-password
FRONTEND_URL=https://claplog.streamlit.app
CORS_ALLOWED_ORIGINS=https://claplog.streamlit.app
```

Railway auto-provides: `DATABASE_URL`, `PORT`

#### 5. Deploy Streamlit Frontend on Streamlit Cloud

1. Go to https://share.streamlit.io
2. Click "New app"
3. Repository: `mudita15sharma/ClapLog`
4. Branch: `main`
5. Main file path: `streamlit_app/app.py`
6. Click "Deploy"

#### 6. Add Secrets to Streamlit Cloud

In Streamlit Cloud dashboard → Your app → Settings → Secrets:

```toml
[api]
base_url = "https://your-railway-app.up.railway.app/api"
```

Update `streamlit_app/api/client.py`:
```python
import streamlit as st

class APIClient:
    def __init__(self):
        # Check if running on Streamlit Cloud
        try:
            self.base_url = st.secrets["api"]["base_url"]
        except:
            # Local development
            self.base_url = "http://127.0.0.1:8000/api"
```

---

## Option 2: Render (Alternative Free Option)

### Django Backend on Render

1. Go to https://render.com
2. New → Web Service → Connect GitHub repo
3. Settings:
   - Build Command: `pip install -r requirements-deploy.txt`
   - Start Command: `gunicorn claplog.wsgi:application`
   - Add PostgreSQL database
   - Add environment variables (same as Railway)

### Streamlit on Streamlit Cloud
Same as above (Step 5-6)

---

## Option 3: Docker (Self-Hosted VPS)

Create `Dockerfile`:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements-deploy.txt .
RUN pip install --no-cache-dir -r requirements-deploy.txt

# Copy project
COPY . .

# Run migrations and start server
CMD python manage.py migrate && \
    gunicorn claplog.wsgi:application --bind 0.0.0.0:$PORT
```

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: claplog
      POSTGRES_USER: claplog_user
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data

  web:
    build: .
    command: gunicorn claplog.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    depends_on:
      - db
    environment:
      - DATABASE_URL=postgresql://claplog_user:${DB_PASSWORD}@db:5432/claplog
      - SECRET_KEY=${SECRET_KEY}
      - DEBUG=False

volumes:
  postgres_data:
```

Deploy to any VPS (DigitalOcean, Linode, AWS EC2):
```bash
docker-compose up -d
```

---

## Post-Deployment Checklist

- [ ] Django admin accessible at `/admin`
- [ ] API endpoints working at `/api/`
- [ ] Streamlit app connects to Django backend
- [ ] User registration + email verification working
- [ ] Database migrations applied
- [ ] Static files serving correctly
- [ ] CORS configured for Streamlit domain
- [ ] Environment variables set correctly
- [ ] HTTPS enabled (Railway/Render provide this automatically)

---

## Troubleshooting

### "DisallowedHost at /"
**Fix:** Add your Railway/Render URL to `ALLOWED_HOSTS` in environment variables

### "CORS error" when Streamlit calls Django
**Fix:** Add Streamlit app URL to `CORS_ALLOWED_ORIGINS`

### Database connection refused
**Fix:** Check `DATABASE_URL` environment variable is set correctly

### Static files not loading
**Fix:** Run `python manage.py collectstatic` and ensure `whitenoise` is in MIDDLEWARE

### Streamlit can't reach Django API
**Fix:** Update `base_url` in Streamlit secrets to point to Railway/Render URL

---

## Costs

| Service | Free Tier | Limits |
|---|---|---|
| Railway | $5 credit/month | ~500 hours/month |
| Render | Free | Spins down after 15min inactivity |
| Streamlit Cloud | Free | Unlimited |

**Total cost for hobby project: $0/month** ✅

---

## Need Help?

- Railway Docs: https://docs.railway.app
- Render Docs: https://render.com/docs
- Streamlit Cloud Docs: https://docs.streamlit.io/streamlit-community-cloud
