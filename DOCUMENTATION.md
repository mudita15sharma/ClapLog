# 📚 ClapLog — Full Technical Documentation

## Table of Contents
1. [Architecture](#architecture)
2. [Backend Deep Dive](#backend-deep-dive)
3. [Frontend Deep Dive](#frontend-deep-dive)
4. [Authentication Flow](#authentication-flow)
5. [Data Flow](#data-flow)
6. [Styling System](#styling-system)
7. [Component Reference](#component-reference)
8. [Common Errors & Fixes](#common-errors--fixes)
9. [Adding New Features](#adding-new-features)
10. [Deployment Guide](#deployment-guide)

---

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                   USER BROWSER                       │
│              http://localhost:8501                   │
└─────────────────────┬───────────────────────────────┘
                       │ HTTP
┌─────────────────────▼───────────────────────────────┐
│              STREAMLIT FRONTEND                      │
│                  app.py                              │
│         pages/ components/ styles/                   │
│                                                      │
│  api/client.py  ──────────────────────────────────► │
└─────────────────────┬───────────────────────────────┘
                       │ REST API (HTTP/JSON)
                       │ Bearer Token (JWT)
┌─────────────────────▼───────────────────────────────┐
│               DJANGO REST API                        │
│           http://localhost:8000/api/                 │
│                                                      │
│  ViewSets → Serializers → Models → ORM              │
└─────────────────────┬───────────────────────────────┘
                       │ SQL
┌─────────────────────▼───────────────────────────────┐
│                  MySQL DATABASE                      │
│                   claplog db                         │
└─────────────────────────────────────────────────────┘
```

---

## Backend Deep Dive

### Django App Structure

Each feature is a separate Django app in `apps/`:

```
apps/
├── users/          → CustomUser model, JWT auth, email verification
├── productions/    → Production model, statistics endpoint
├── scenes/         → Scene model with status workflow
├── shots/          → Shot model with camera specs
├── call_sheets/    → CallSheet model
├── cast/           → CastMember model
├── props/          → Prop model
└── continuity/     → ContinuityNote model
```

### URL Routing

```python
# claplog/urls.py
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('claplog.api_urls')),
]

# claplog/api_urls.py  
router = DefaultRouter()
router.register('productions',    ProductionViewSet)
router.register('scenes',         SceneViewSet)
router.register('shots',          ShotViewSet)
router.register('call-sheets',    CallSheetViewSet)
router.register('cast-members',   CastMemberViewSet)
router.register('props',          PropViewSet)
router.register('continuity-notes', ContinuityNoteViewSet)
```

### Production Serializer — Live Stats

The key pattern for live dashboard stats:

```python
class ProductionSerializer(serializers.ModelSerializer):
    scene_count           = serializers.SerializerMethodField()
    shot_count            = serializers.SerializerMethodField()
    completed_scene_count = serializers.SerializerMethodField()

    def get_scene_count(self, obj):
        return obj.scenes.count()

    def get_shot_count(self, obj):
        return sum(s.shots.count() for s in obj.scenes.all())

    def get_completed_scene_count(self, obj):
        return obj.scenes.filter(status='completed').count()
```

### ViewSet Pattern

Every ViewSet follows this pattern:

```python
class SceneViewSet(viewsets.ModelViewSet):
    serializer_class   = SceneSerializer
    permission_classes = [IsAuthenticated]
    filter_backends    = [DjangoFilterBackend]
    filterset_fields   = ['production', 'status']

    def get_queryset(self):
        # Always filter by current user's productions
        return Scene.objects.filter(
            production__created_by=self.request.user
        )

    def perform_create(self, serializer):
        serializer.save()
```

### Scene Status Workflow

```python
# apps/scenes/models.py
class Scene(models.Model):
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed',   'Completed'),
        ('on_hold',     'On Hold'),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='not_started'
    )
```

Changing a scene to `completed` via `PATCH /api/scenes/{id}/`
automatically updates the production's completion percentage
because the serializer calculates it live on every request.

---

## Frontend Deep Dive

### API Client (`streamlit_app/api/client.py`)

All HTTP calls go through `APIClient`:

```python
class APIClient:
    def __init__(self):
        self.base_url = "http://127.0.0.1:8000/api"
        self.token = None

    def get_productions(self):
        response = requests.get(
            f"{self.base_url}/productions/",
            headers={"Authorization": f"Bearer {self.token}"}
        )
        if response.status_code == 200:
            data = response.json()
            return data.get('results', data)
        return []
```

### Session State

Streamlit uses `st.session_state` as a global store:

```python
# Initialized in app.py
st.session_state.authenticated = False   # bool
st.session_state.token = None            # JWT string
st.session_state.user = None             # user dict
st.session_state.selected_production = None  # production dict
```

### Page Authentication Guard

Every page starts with:

```python
if not st.session_state.get('authenticated', False):
    st.warning("⚠️ Please login first")
    st.switch_page("app.py")
    st.stop()
```

### Production Selector Component

```python
# Used on all pages except Productions
from components.production_selector import show_production_selector

production = show_production_selector(api)
if not production:
    st.info("👆 Select a production to continue")
    st.stop()

# Now use production['id'] for API calls
```

---

## Authentication Flow

```
REGISTRATION:
User fills form → POST /api/auth/register/
    → Django creates user (is_active=False)
    → Sends verification email with JWT token
    → User clicks link → GET /api/auth/verify-email/?token=xxx
    → Django sets is_active=True
    → User can now login

LOGIN:
POST /api/auth/login/ with username + password
    → Returns: { access: "eyJ...", refresh: "eyJ..." }
    → Streamlit stores access token in session_state
    → All subsequent requests include: Authorization: Bearer eyJ...

TOKEN USAGE:
Every API call includes the Bearer token
Django validates it via SimpleJWT middleware
If expired → 401 → Streamlit redirects to login
```

---

## Data Flow

### Dashboard Live Stats

```
1. User opens dashboard
2. api.get_productions() → GET /api/productions/
3. Django ProductionViewSet.get_queryset()
   → filters by created_by=request.user
   → prefetch_related('scenes', 'scenes__shots')
4. ProductionSerializer runs for each production:
   → get_scene_count()     → obj.scenes.count()
   → get_shot_count()      → sum of shots per scene
   → get_completed_scene_count() → scenes.filter(status='completed').count()
5. Returns JSON list with all counts included
6. Streamlit calculates:
   → total_scenes = sum(p['scene_count'] for p in productions)
   → completion = done_scenes / total_scenes * 100
7. Renders metric cards and progress bars with real data
```

### Scene Status Update → Dashboard Update

```
User on Scenes page:
1. Selects scene → changes status to "completed"
2. PATCH /api/scenes/{id}/ with {status: "completed"}
3. Django updates scene in database
4. User goes to Dashboard
5. api.get_productions() runs fresh
6. get_completed_scene_count() now returns +1
7. Dashboard shows updated completion %
```

---

## Styling System

### Theme File (`streamlit_app/styles/dark_theme.py`)

```python
def apply_dark_theme():
    """Call at the top of every page."""
    set_background_image()  # random background from assets/
    st.markdown(css, unsafe_allow_html=True)
```

### Color Palette

```css
--primary-color:    #3b82f6;   /* Blue - buttons, borders */
--accent-color:     #06b6d4;   /* Cyan - labels, stats */
--accent-glow:      #22d3ee;   /* Bright cyan - glows, highlights */
--background-color: #0a0e14;   /* Deep blue-black */
--secondary-bg:     #151b24;   /* Dark slate */
--card-bg:          #1e2936;   /* Card backgrounds */
--text-color:       #ffffff;   /* White text */
--success-color:    #10b981;   /* Green */
--error-color:      #ef4444;   /* Red */
```

### Font Hierarchy

```
Tangerine (cursive)     → H1, H2, page titles, logo text
Dancing Script          → H3, H4, card titles, subheadings
Inter (sans-serif)      → Everything else: body, buttons, inputs, tables
```

### Streamlit HTML Limitations

Streamlit's sanitizer STRIPS these CSS properties:
- `display: flex` / `display: grid`
- `position: absolute/fixed`
- `justify-content`, `align-items`

Use these instead:
- `st.columns()` for side-by-side layout
- `st.container(border=True)` for cards
- `st.progress()` for progress bars
- `<table>` HTML for simple 2-column layouts

---

## Component Reference

### `logo.py`

```python
from components.logo import show_logo, show_logo_in_header

show_logo()           # Sidebar logo (all authenticated pages)
show_logo_in_header() # Centered header logo (login page only)
```

Logo search order: `Logo.jpg → Logo.png → Logogif.gif → logogif.gif`
Uses base64 embedding — no path/serving issues.

### `visuals.py`

```python
from components.visuals import show_random_film_quote, show_film_strip_divider

show_random_film_quote()   # Random cinema quote in styled box
show_film_strip_divider()  # Decorative divider line
```

### `animations.py`

```python
from components.animations import show_success_clapper

show_success_clapper("Login Successful!")  # Animated success message
```

### `production_selector.py`

```python
from components.production_selector import show_production_selector

production = show_production_selector(api)
# Returns selected production dict or None
# Shows selectbox with all user's productions
```

---

## Common Errors & Fixes

### ImportError: circular import in logo.py
**Cause:** `logo.py` importing from itself  
**Fix:** Remove any `from components.logo import ...` inside `logo.py`

### KeyError on shot/scene fields
**Cause:** API returning dict without expected key  
**Fix:** Always use `.get()`: `shot.get('frame_rate', 'N/A')`

### `use_container_width` TypeError
**Cause:** Old Streamlit version compatibility  
**Fix:**
- `st.image()` → `use_column_width=True`
- `st.button()` → `use_container_width=True`

### 404 on API endpoint
**Cause:** Endpoint not registered in `api_urls.py`  
**Fix:** Add `router.register('endpoint-name', ViewSet)` to `api_urls.py`

### 400 Bad Request on POST
**Cause:** Missing required fields or wrong data types  
**Fix:** Check serializer required fields, ensure IDs are integers not strings

### HTML showing as raw text in Streamlit
**Cause:** Streamlit sanitizer stripping CSS  
**Fix:** Use native `st.columns()`, `st.container()`, `st.progress()` instead of HTML divs

### Django ImportError: cannot import ProductionTeamViewSet
**Cause:** `urls.py` imports a class that doesn't exist in `views.py`  
**Fix:** Add stub class to `views.py` or remove import from `urls.py`

---

## Adding New Features

### Adding a New Page

1. Create `streamlit_app/pages/MyFeature.py`:

```python
import streamlit as st
import sys
from pathlib import Path

parent_dir = Path(__file__).parent.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

from api.client import APIClient
from styles.dark_theme import apply_dark_theme
from components.production_selector import show_production_selector

st.set_page_config(page_title="My Feature - ClapLog", page_icon="🎯", layout="wide")
apply_dark_theme()
api = APIClient()
api.token = st.session_state.get('token')

# Auth guard
if not st.session_state.get('authenticated', False):
    st.warning("⚠️ Please login first")
    st.switch_page("app.py")
    st.stop()

st.markdown("# My Feature")

production = show_production_selector(api)
if not production:
    st.info("👆 Select a production to continue")
    st.stop()

# Your feature code here
```

2. Add to sidebar navigation automatically (Streamlit auto-discovers `pages/`)

### Adding a New API Endpoint

1. Create model in `apps/myfeature/models.py`
2. Create serializer in `apps/myfeature/serializers.py`
3. Create viewset in `apps/myfeature/views.py`
4. Register in `claplog/api_urls.py`:
```python
router.register('my-features', MyFeatureViewSet)
```
5. Add client method in `streamlit_app/api/client.py`
6. Run `python manage.py makemigrations && python manage.py migrate`

---

## Deployment Guide

### Option 1: Streamlit Community Cloud (Free)

1. Push to GitHub (public repo)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect GitHub → select repo → set main file: `streamlit_app/app.py`
4. Add secrets in Streamlit Cloud dashboard

⚠️ **Note:** You still need Django hosted separately (Railway, Render, etc.)

### Option 2: Railway (Full Stack, Free tier)

```bash
# Install Railway CLI
npm install -g @railway/cli
railway login
railway new

# Deploy Django
railway add --plugin mysql
railway up

# Set environment variables in Railway dashboard
```

### Option 3: Docker (Self-hosted)

```dockerfile
# Dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000 8501
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000 & streamlit run streamlit_app/app.py --server.port 8501 --server.address 0.0.0.0"]
```

### Environment Variables for Production

```env
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=mysql://user:pass@host:3306/claplog
SECRET_KEY=very-long-random-production-key
FRONTEND_URL=https://yourdomain.com
```

---

*Documentation last updated: February 2026*
*ClapLog v1.0 — Built with Django 5.0.1 + Streamlit*
