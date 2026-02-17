"""
Shots page - Manage camera shots.
"""

import sys
import streamlit as st
from pathlib import Path

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
    page_title="Shots - ClapLog",
    page_icon="📷",
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

st.markdown("# 📷 Shots")
show_page_quote("Shots")

production = show_production_selector(api)

if not production:
    st.info("👆 Please select a production above to continue")
    st.stop()

st.markdown(f"### 📷 Shots for: **{production['title']}**")

scenes = api.get_scenes(production['id'])

tab1, tab2 = st.tabs(["📷 All Shots", "➕ Create Shot"])

with tab1:
    st.markdown("### 📷 All Shots")

    if not scenes:
        st.warning("⚠️ No scenes found. Please create scenes first.")
        if st.button("➕ Go to Scenes Page"):
            st.switch_page("pages/2_📋_Scenes.py")
        st.stop()

    scene_options = ["All Scenes"] + [f"Scene {s.get('scene_number', 'N/A')} - {s.get('location_text', 'Unnamed')}" for
                                      s in scenes]
    scene_filter = st.selectbox("Filter by Scene", scene_options)

    if scene_filter == "All Scenes":
        all_shots = []
        for scene in scenes:
            scene_shots = api.get_shots(scene['id'])
            if scene_shots:
                all_shots.extend(scene_shots)
        shots = all_shots
    else:
        scene_index = scene_options.index(scene_filter) - 1
        selected_scene = scenes[scene_index]
        shots = api.get_shots(selected_scene['id'])

    if shots:
        st.write(f"**Total: {len(shots)} shots**")

        for shot in shots:
            shot_num = shot.get('shot_number', 'N/A')
            shot_type = shot.get('shot_type', 'N/A')

            with st.expander(f"Shot {shot_num} - {shot_type}", expanded=False):
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.write(f"**Shot Number:** {shot_num}")
                    st.write(f"**Type:** {shot_type}")
                    st.write(f"**Angle:** {shot.get('camera_angle', 'N/A')}")
                    st.write(f"**Movement:** {shot.get('camera_movement', 'N/A')}")

                with col2:
                    status = shot.get('status', 'not_started')
                    st.write(f"**Status:** {status.replace('_', ' ').title()}")
                    st.write(f"**Takes Completed:** {shot.get('takes_completed', 0)}")
                    st.write(f"**Takes Planned:** {shot.get('takes_planned', 0)}")
                    st.write(f"**Frame Rate:** {shot.get('frame_rate', 24)} fps")

                with col3:
                    st.write(f"**Lens:** {shot.get('lens') or 'N/A'}")
                    st.write(f"**Aperture:** {shot.get('aperture') or 'N/A'}")
                    st.write(f"**ISO:** {shot.get('iso') or 'N/A'}")
                    st.write(f"**VFX Required:** {'Yes' if shot.get('vfx_required') else 'No'}")

                if shot.get('description'):
                    st.write(f"**Description:**")
                    st.info(shot['description'])

                if shot.get('notes'):
                    st.write(f"**Notes:**")
                    st.info(shot['notes'])

                col_a, col_b = st.columns(2)
                with col_a:
                    if st.button("✏️ Edit", key=f"edit_{shot.get('id')}"):
                        st.info("Edit functionality coming soon!")
                with col_b:
                    if st.button("🗑️ Delete", key=f"delete_{shot.get('id')}"):
                        st.warning("Delete functionality coming soon!")
    else:
        st.info("📷 No shots found. Create your first shot below!")

with tab2:
    st.markdown("### ➕ Create New Shot")

    if not scenes:
        st.warning("⚠️ Please create scenes first!")
        if st.button("➕ Go to Scenes Page", key="create_scene_btn"):
            st.switch_page("pages/2_📋_Scenes.py")
        st.stop()

    with st.form("create_shot_form"):
        scene_options = {f"Scene {s.get('scene_number', 'N/A')} - {s.get('location_text', 'Unnamed')}": s['id'] for s in
                         scenes}
        selected_scene = st.selectbox("📋 Scene *", list(scene_options.keys()))

        col1, col2 = st.columns(2)

        with col1:
            shot_number = st.text_input(
                "📷 Shot Number *",
                placeholder="e.g., 1, 2A, 15-1",
                help="Unique identifier for this shot"
            )
            shot_name = st.text_input(
                "Shot Name",
                placeholder="Optional descriptive name"
            )

            shot_type = st.selectbox("🎥 Shot Type *", [
                "WIDE",
                "MEDIUM",
                "CLOSE_UP",
                "EXTREME_CLOSE_UP",
                "TWO_SHOT",
                "OVER_SHOULDER",
                "POV",
                "INSERT",
                "ESTABLISHING",
                "MASTER"
            ], format_func=lambda x: x.replace('_', ' ').title())

            camera_angle = st.selectbox("📐 Camera Angle *", [
                "EYE_LEVEL",
                "HIGH_ANGLE",
                "LOW_ANGLE",
                "DUTCH_ANGLE",
                "AERIAL",
                "BIRDS_EYE"
            ], format_func=lambda x: x.replace('_', ' ').title())

            camera_movement = st.selectbox("🎬 Camera Movement *", [
                "STATIC",
                "PAN",
                "TILT",
                "DOLLY",
                "TRACKING",
                "CRANE",
                "HANDHELD",
                "STEADICAM",
                "ZOOM"
            ], format_func=lambda x: x.title())

        with col2:
            lens = st.text_input("🔍 Lens", placeholder="e.g., 50mm, 24-70mm")
            aperture = st.text_input("📹 Aperture", placeholder="e.g., f/2.8")
            iso = st.text_input("💡 ISO", placeholder="e.g., 800")
            frame_rate = st.number_input("🎞️ Frame Rate (fps)", min_value=1, max_value=120, value=24)

            status = st.selectbox("📊 Status", [
                "not_started",
                "in_progress",
                "completed",
                "rejected",
                "approved"
            ], format_func=lambda x: x.replace('_', ' ').title())

        description = st.text_area(
            "📝 Description",
            placeholder="Describe the shot composition, action, and purpose..."
        )
        notes = st.text_area(
            "📋 Notes",
            placeholder="Technical notes, special requirements, etc..."
        )

        col_a, col_b = st.columns(2)
        with col_a:
            vfx_required = st.checkbox("✨ VFX Required")
        with col_b:
            takes_planned = st.number_input("🎬 Takes Planned", min_value=1, max_value=50, value=3)

        submit = st.form_submit_button("📷 Create Shot", use_container_width=True, type="primary")

        if submit:
            if not shot_number:
                st.error("⚠️ Shot number is required!")
            else:
                data = {
                    "scene": scene_options[selected_scene],
                    "shot_number": shot_number,
                    "shot_name": shot_name or "",
                    "shot_type": shot_type,
                    "camera_angle": camera_angle,
                    "camera_movement": camera_movement,
                    "lens": lens or "",
                    "aperture": aperture or "",
                    "iso": iso or "",
                    "frame_rate": frame_rate,
                    "status": status,
                    "description": description or "",
                    "notes": notes or "",
                    "vfx_required": vfx_required,
                    "takes_planned": takes_planned
                }

                with st.spinner("Creating shot..."):
                    result = api.create_shot(data)

                if result:
                    show_success_clapper("Shot Created!")
                    st.success(f"✅ Shot {shot_number} created successfully!")
                    st.balloons()
                    st.rerun()
                else:
                    st.error("❌ Failed to create shot. Please try again.")


st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #888; font-size: 0.9rem;">
    💡 **Tip:** Plan your shots carefully - good coverage saves time in post-production!
</div>
""", unsafe_allow_html=True)