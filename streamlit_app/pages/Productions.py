"""
Productions page - Manage film productions.
"""

import streamlit as st
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from api.client import APIClient
from styles.dark_theme import apply_dark_theme
from components.visuals import show_film_strip_divider, show_page_quote
from components.animations import show_success_clapper
from components.production_selector import show_production_selector
from components.logo import show_logo

st.set_page_config(
    page_title="Productions - ClapLog",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)
apply_dark_theme()

api = APIClient()
api.token = st.session_state.get('token')

if not st.session_state.get('authenticated', False):
    st.warning("Please login first")
    if st.button("Go to Login"):
        st.switch_page("app.py")
    st.stop()

st.title("🎬 Productions")

show_logo()
show_page_quote("Productions")

tab1, tab2 = st.tabs(["📋 All Productions", "➕ Create New"])

with tab1:
    st.subheader("Your Productions")

    productions = api.get_productions()

    if productions:

        for prod in productions:
            with st.expander(f"🎬 {prod['title']}", expanded=False):
                col1, col2 = st.columns(2)

                new_status = st.selectbox("Update Status", [
                    "development", "pre_production",
                    "in_production", "post_production", "completed"
                ], key=f"prod_status_{prod['id']}")

                if st.button("💾 Update", key=f"update_prod_{prod['id']}"):
                    api.update_production(prod['id'], {"status": new_status})
                    st.success("Updated!")
                    st.rerun()

                with col1:
                    st.write(f"**Director:** {prod.get('director') or 'N/A'}")
                    st.write(f"**Company:** {prod.get('production_company') or 'N/A'}")
                    st.write(f"**Status:** {prod.get('status', '').replace('_', ' ').title()}")
                    st.write(f"**Genre:** {prod.get('genre') or 'N/A'}")

                with col2:
                    st.write(f"**Start Date:** {prod.get('start_date') or 'N/A'}")
                    st.write(f"**End Date:** {prod.get('end_date') or 'N/A'}")
                    st.write(f"**Budget:** ${prod.get('budget') or '0'}")
                    st.write(f"**Team Size:** {prod.get('team_count', 0)}")

                if prod.get('description'):
                    st.write(f"**Description:** {prod['description']}")

                st.divider()
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    st.metric("Scenes", prod.get('scene_count', 0))
                with col_b:
                    st.metric("Completion", f"{prod.get('completion_percentage', 0):.1f}%")
                with col_c:
                    if st.button("📊 View Details", key=f"view_{prod['id']}"):
                        st.session_state.selected_production = prod
                        st.success(f"Selected: {prod['title']}")
    else:
        st.info("No productions found. Create your first production!")

with tab2:
    st.subheader("Create New Production")

    with st.form("create_production_form"):
        col1, col2 = st.columns(2)

        with col1:
            title = st.text_input("Production Title *", placeholder="Enter production title")
            director = st.text_input("Director", placeholder="Director name")
            production_company = st.text_input("Production Company", placeholder="Company name")
            genre = st.text_input("Genre", placeholder="e.g., Drama, Action, Comedy")

        with col2:
            status = st.selectbox("Status", [
                "pre_production",
                "production",
                "post_production",
                "completed"
            ], format_func=lambda x: x.replace('_', ' ').title())

            start_date = st.date_input("Start Date")
            end_date = st.date_input("End Date")
            budget = st.number_input("Budget ($)", min_value=0, value=0, step=1000)

        description = st.text_area("Description", placeholder="Brief description of the production")

        col_a, col_b = st.columns(2)
        with col_a:
            runtime_minutes = st.number_input("Runtime (minutes)", min_value=0, value=90)
        with col_b:
            aspect_ratio = st.text_input("Aspect Ratio", value="16:9", placeholder="e.g., 16:9, 2.35:1")

        submit = st.form_submit_button("🎬 Create Production", use_container_width=True)

        if submit:
            if not title:
                st.error("Production title is required!")
            else:
                data = {
                    "title": title,
                    "director": director,
                    "production_company": production_company,
                    "status": status,
                    "start_date": str(start_date) if start_date else None,
                    "end_date": str(end_date) if end_date else None,
                    "budget": str(budget) if budget > 0 else None,
                    "description": description,
                    "genre": genre,
                    "runtime_minutes": runtime_minutes if runtime_minutes > 0 else None,
                    "aspect_ratio": aspect_ratio
                }

                result = api.create_production(data)
                if result:
                    show_success_clapper("Welcome in New Production !!!")
                    st.success(f"✅ Production '{title}' created successfully!")
                    st.balloons()
                    st.rerun()


st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #888; font-size: 0.9rem;">
    💡 **Tip:** Happy Producing !!
</div>
""", unsafe_allow_html=True)

