"""
Scenes page - Manage scenes in production.
"""

import sys
import streamlit as st
from pathlib import Path

from streamlit_app.components.logo import show_logo

parent_dir = Path(__file__).parent.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

from api.client import APIClient
from styles.dark_theme import apply_dark_theme
from components.visuals import show_film_strip_divider, show_page_quote
from components.animations import show_success_clapper
from components.production_selector import show_production_selector
from components.logo import show_logo

st.set_page_config(
    page_title="Scenes - ClapLog",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_dark_theme()

api = APIClient()
api.token = st.session_state.get('token')

if not st.session_state.get('authenticated', False):
    st.warning("⚠️ Please login first")
    st.switch_page("app.py")
    st.stop()

show_logo()

st.markdown("# 📋 Scenes")
show_page_quote("Scenes")

production = show_production_selector(api)

if not production:
    st.info("👆 Please select a production above to continue")
    st.stop()

st.markdown(f"### 📋 Scenes for: **{production['title']}**")

tab1, tab2 = st.tabs(["📋 All Scenes", "➕ Create Scene"])

with tab1:
    st.markdown("### 📋 All Scenes")

    col1, col2, col3 = st.columns(3)
    with col1:
        filter_status = st.selectbox("Filter by Status", [
            "All",
            "not_started",
            "in_progress",
            "completed",
            "on_hold"
        ], format_func=lambda x: x.replace('_', ' ').title())

    with col2:
        filter_int_ext = st.selectbox("Filter by INT/EXT", [
            "All", "INT", "EXT", "INT/EXT"
        ])

    with col3:
        filter_day_night = st.selectbox("Filter by Time", [
            "All", "DAY", "NIGHT", "DAWN", "DUSK"
        ])

    scenes = api.get_scenes(production['id'])

    if scenes:
        if filter_status != "All":
            scenes = [s for s in scenes if s.get('status') == filter_status]
        if filter_int_ext != "All":
            scenes = [s for s in scenes if s.get('interior_exterior') == filter_int_ext]
        if filter_day_night != "All":
            scenes = [s for s in scenes if s.get('day_night') == filter_day_night]

    if scenes:
        st.write(f"**Total: {len(scenes)} scenes**")

        for scene in scenes:
            with st.expander(
                    f"Scene {scene.get('scene_number', 'N/A')} - {scene.get('scene_name') or scene.get('location_text', 'Unnamed')}",
                    expanded=False
            ):
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.write(f"**Location:** {scene.get('location_text') or 'N/A'}")
                    st.write(f"**INT/EXT:** {scene.get('interior_exterior', 'N/A')}")
                    st.write(f"**Day/Night:** {scene.get('day_night', 'N/A')}")

                with col2:
                    st.write(f"**Status:** {scene.get('status', '').replace('_', ' ').title()}")
                    st.write(f"**Script Pages:** {scene.get('script_pages') or 'N/A'}")
                    st.write(f"**Shooting Date:** {scene.get('shooting_date') or 'Not scheduled'}")

                with col3:
                    st.write(f"**Shots:** {scene.get('shot_count', 0)}")
                    st.write(f"**Priority:** {scene.get('priority', 0)}")

                if scene.get('description'):
                    st.write(f"**Description:** {scene['description']}")

                if scene.get('notes'):
                    st.write(f"**Notes:** {scene['notes']}")

                col_a, col_b = st.columns(2)
                with col_a:
                    if st.button("✏️ Edit", key=f"edit_{scene['id']}"):
                        st.info("Edit functionality coming soon!")
                with col_b:
                    if st.button("🗑️ Delete", key=f"delete_{scene['id']}"):
                        st.warning("Delete functionality coming soon!")
    else:
        st.info("📋 No scenes found. Create your first scene!")

with tab2:
    st.markdown("### ➕ Create New Scene")

    with st.form("create_scene_form"):
        col1, col2 = st.columns(2)

        with col1:
            scene_number = st.text_input("Scene Number *", placeholder="e.g., 1, 2A, 15")
            scene_name = st.text_input("Scene Name", placeholder="Optional scene name")
            location_text = st.text_input("Location *", placeholder="e.g., COFFEE SHOP, PARK")

            interior_exterior = st.selectbox("INT/EXT", ["INT", "EXT", "INT/EXT"])
            day_night = st.selectbox("Day/Night", ["DAY", "NIGHT", "DAWN", "DUSK", "CONTINUOUS"])

        with col2:
            script_pages = st.number_input("Script Pages", min_value=0.1, max_value=20.0, value=1.0, step=0.125)
            estimated_duration = st.number_input("Estimated Duration (minutes)", min_value=1, value=5)

            status = st.selectbox("Status", [
                "not_started",
                "in_progress",
                "completed",
                "on_hold"
            ], format_func=lambda x: x.replace('_', ' ').title())

            shooting_date = st.date_input("Shooting Date (optional)")
            priority = st.slider("Priority", 0, 10, 5)

        description = st.text_area("Description", placeholder="Scene description or action")

        col_a, col_b, col_c = st.columns(3)
        with col_a:
            vfx_required = st.checkbox("VFX Required")
        with col_b:
            stunts_required = st.checkbox("Stunts Required")
        with col_c:
            weather_dependent = st.checkbox("Weather Dependent")

        notes = st.text_area("Notes", placeholder="Additional notes")

        submit = st.form_submit_button("📋 Create Scene", use_container_width=True)

        if submit:
            if not scene_number or not location_text:
                st.error("⚠️ Scene number and location are required!")
            else:
                data = {
                    "production": production['id'],
                    "scene_number": scene_number,
                    "scene_name": scene_name,
                    "location_text": location_text,
                    "interior_exterior": interior_exterior,
                    "day_night": day_night,
                    "script_pages": str(script_pages),
                    "estimated_duration": estimated_duration,
                    "status": status,
                    "shooting_date": str(shooting_date) if shooting_date else None,
                    "priority": priority,
                    "description": description,
                    "vfx_required": vfx_required,
                    "stunts_required": stunts_required,
                    "weather_dependent": weather_dependent,
                    "notes": notes
                }

                with st.spinner("Creating scene..."):
                    result = api.create_scene(data)

                if result:
                    show_success_clapper("Scene Created!")
                    st.success(f"✅ Scene {scene_number} created successfully!")
                    st.balloons()
                    st.rerun()
                else:
                    st.error("❌ Failed to create scene. Please try again.")

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #888; font-size: 0.9rem;">
    💡 **Tip:** Break down your script scene by scene for better planning!
</div>
""", unsafe_allow_html=True)