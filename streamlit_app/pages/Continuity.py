"""
Continuity Notes Page - Track continuity details across scenes.

This page allows script supervisors and crew to document:
- Costume continuity
- Props placement
- Actor positioning
- Lighting setup
- Camera angles
- Any other continuity-critical details
"""

import streamlit as st
import sys
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
    page_title="Continuity - ClapLog",
    page_icon="✅",
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

st.markdown("# ✅ Continuity Tracking")
show_page_quote("Continuity")

production = show_production_selector(api)

if not production:
    st.info("👆 Please select a production above to continue")
    st.stop()

st.markdown(f"### ✅ Continuity Notes for: **{production['title']}**")

scenes = api.get_scenes(production['id'])

tab1, tab2 = st.tabs(["📝 All Notes", "➕ Add Note"])

with tab1:
    st.markdown("### 📝 All Continuity Notes")

    notes = api.get_continuity_notes(production['id'])

    if notes:
        st.markdown("#### 🔍 Filters")
        col1, col2, col3 = st.columns(3)

        with col1:
            filter_category = st.selectbox(
                "Category",
                ["All", "costume", "props", "makeup", "hair", "lighting", "camera", "script", "other"]
            )
        with col2:
            filter_severity = st.selectbox(
                "Severity",
                ["All", "low", "medium", "high", "critical"]
            )
        with col3:
            filter_status = st.selectbox(
                "Status",
                ["All", "active", "resolved", "flagged", "archived"]
            )

        filtered_notes = notes
        if filter_category != "All":
            filtered_notes = [n for n in filtered_notes if n.get('category') == filter_category]
        if filter_severity != "All":
            filtered_notes = [n for n in filtered_notes if n.get('severity') == filter_severity]
        if filter_status != "All":
            filtered_notes = [n for n in filtered_notes if n.get('status') == filter_status]

        st.write(f"**Showing {len(filtered_notes)} of {len(notes)} notes**")

        for note in filtered_notes:
            severity_colors = {
                'low': '🟢',
                'medium': '🟡',
                'high': '🟠',
                'critical': '🔴'
            }

            status_icons = {
                'active': '📌',
                'resolved': '✅',
                'flagged': '🚩',
                'archived': '📦'
            }

            severity_icon = severity_colors.get(note.get('severity', 'low'), '🟢')
            status_icon = status_icons.get(note.get('status', 'active'), '📌')

            scene_num = "N/A"
            if note.get('scene'):
                # Find the scene in our scenes list
                scene = next((s for s in scenes if s['id'] == note['scene']), None)
                if scene:
                    scene_num = scene.get('scene_number', 'N/A')

            with st.expander(
                f"{severity_icon} {status_icon} {note.get('category', '').title()} - Scene {scene_num}",
                expanded=False
            ):
                col1, col2 = st.columns(2)

                with col1:
                    st.write(f"**Category:** {note.get('category', '').title()}")
                    st.write(f"**Severity:** {note.get('severity', '').title()}")
                    st.write(f"**Status:** {note.get('status', '').title()}")

                with col2:
                    if note.get('actor_character'):
                        st.write(f"**Actor/Character:** {note['actor_character']}")
                    created = note.get('created_at', '')
                    if created:
                        st.write(f"**Created:** {created[:10]}")

                st.write(f"**Description:**")
                st.info(note.get('description', 'No description'))

                if note.get('warnings'):
                    st.warning(f"⚠️ **Warning:** {note['warnings']}")

                col_a, col_b, col_c = st.columns(3)

                with col_a:
                    if st.button("✅ Mark Resolved", key=f"resolve_{note['id']}"):
                        update_data = {"status": "resolved"}
                        if api.update_continuity_note(note['id'], update_data):
                            show_success_clapper("Note Resolved!")
                            st.rerun()

                with col_b:
                    if st.button("🚩 Flag", key=f"flag_{note['id']}"):
                        update_data = {"status": "flagged"}
                        if api.update_continuity_note(note['id'], update_data):
                            show_success_clapper("Note Flagged!")
                            st.rerun()

                with col_c:
                    if st.button("🗑️ Delete", key=f"delete_{note['id']}"):
                        if api.delete_continuity_note(note['id']):
                            show_success_clapper("Note Deleted!")
                            st.rerun()
    else:
        st.info("📝 No continuity notes yet. Add your first note below!")


with tab2:
    st.markdown("### ➕ Add Continuity Note")

    if not scenes:
        st.warning("⚠️ No scenes found. Please create scenes first.")
        if st.button("➕ Go to Scenes Page"):
            st.switch_page("pages/Scenes.py")
        st.stop()

    with st.form("add_note_form"):
        scene_options = {f"Scene {s['scene_number']}": s['id'] for s in scenes}
        selected_scene = st.selectbox(
            "📋 Scene *",
            list(scene_options.keys()),
            help="Which scene does this note apply to?"
        )
        scene_id = scene_options[selected_scene]

        col1, col2 = st.columns(2)

        with col1:
            category = st.selectbox(
                "📁 Category *",
                ["costume", "props", "makeup", "hair", "lighting", "camera", "script", "other"],
                format_func=lambda x: x.title(),
                help="What type of continuity issue?"
            )
            severity = st.selectbox(
                "⚠️ Severity *",
                ["low", "medium", "high", "critical"],
                format_func=lambda x: x.title(),
                help="How important is this?"
            )

        with col2:
            status = st.selectbox(
                "📊 Status",
                ["active", "resolved", "flagged", "archived"],
                format_func=lambda x: x.title()
            )
            actor_character = st.text_input(
                "🎭 Actor/Character",
                placeholder="e.g., John Doe as Detective Smith",
                help="Who is this note about?"
            )

        description = st.text_area(
            "📝 Description *",
            placeholder="Detailed continuity note...\n\nExample:\n- Actor wearing blue shirt in Scene 3\n- Coffee cup on left side of table\n- Hair parted on right side",
            height=150,
            help="Detailed description of the continuity detail"
        )

        warnings = st.text_area(
            "⚠️ Warnings/Special Attention",
            placeholder="Any special warnings or notes for the crew...\n\nExample:\n- Critical for matching previous scenes\n- Check with director before changing\n- Must match Scene 1 exactly",
            help="Important warnings for the crew"
        )

        submit = st.form_submit_button(
            "➕ Add Continuity Note",
            use_container_width=True,
            type="primary"
        )

        if submit:
            if not description:
                st.error("⚠️ Description is required")
            else:
                note_data = {
                    "scene": scene_id,
                    "category": category,
                    "severity": severity,
                    "status": status,
                    "description": description,
                    "actor_character": actor_character if actor_character else "",
                    "warnings": warnings if warnings else ""
                }

                with st.spinner("Adding continuity note..."):
                    result = api.create_continuity_note(note_data)

                if result:
                    show_success_clapper("Continuity Note Added!")
                    st.success("✅ Continuity note added successfully!")
                    st.balloons()
                    st.rerun()
                else:
                    st.error("❌ Failed to add note. Please try again.")


st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #888; font-size: 0.9rem;">
    💡 **Tip:** Document everything! Small details can save hours in post-production.
</div>
""", unsafe_allow_html=True)