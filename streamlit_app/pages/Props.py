"""
Props Management Page
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
from components.production_selector import show_production_selector, require_production
from components.logo import show_logo

st.set_page_config(
    page_title="Props - ClapLog",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state = "expanded",)

apply_dark_theme()

api = APIClient()
api.token = st.session_state.get('token')

if not st.session_state.get('authenticated'):
    st.warning("⚠️ Please login first")
    st.switch_page("app.py")

show_logo()

st.markdown("# 📦 Props Management")
show_page_quote("Props")

production = show_production_selector(api)

if production:
    tab1, tab2 = st.tabs(["📦 All Props", "➕ Add Prop"])

    with tab1:
        st.markdown("### 📦 Props Inventory")

        props = api.get_props(production['id'])

        if props:
            col1, col2, col3 = st.columns(3)
            with col1:
                filter_category = st.selectbox(
                    "Category",
                    ["All"] + list(set([p.get('category', '') for p in props]))
                )
            with col2:
                filter_status = st.selectbox(
                    "Status",
                    ["All", "needed", "sourced", "purchased", "rented", "ready", "on_set", "returned"]
                )
            with col3:
                show_hero_only = st.checkbox("🌟 Hero Props Only")

            filtered_props = props
            if filter_category != "All":
                filtered_props = [p for p in filtered_props if p.get('category') == filter_category]
            if filter_status != "All":
                filtered_props = [p for p in filtered_props if p.get('status') == filter_status]
            if show_hero_only:
                filtered_props = [p for p in filtered_props if p.get('hero_prop')]

            for prop in filtered_props:
                status_icons = {
                    'needed': '❗',
                    'sourced': '🔍',
                    'purchased': '💰',
                    'rented': '📋',
                    'ready': '✅',
                    'on_set': '🎬',
                    'returned': '↩️'
                }

                with st.expander(f"{status_icons.get(prop.get('status', ''), '📦')} {prop['name']}" +
                                 (" 🌟" if prop.get('hero_prop') else "")):
                    col1, col2 = st.columns(2)

                    with col1:
                        st.write(f"**Category:** {prop.get('category', '').replace('_', ' ').title()}")
                        st.write(f"**Quantity:** {prop.get('quantity', 1)}")
                        st.write(f"**Status:** {prop.get('status', '').replace('_', ' ').title()}")
                        if prop.get('cost'):
                            st.write(f"**Cost:** ${prop['cost']}")

                    with col2:
                        if prop.get('source'):
                            st.write(f"**Source:** {prop['source']}")
                        if prop.get('brand_model'):
                            st.write(f"**Brand/Model:** {prop['brand_model']}")
                        if prop.get('is_rented') and prop.get('rental_return_date'):
                            st.write(f"**Return Date:** {prop['rental_return_date']}")

                    if prop.get('description'):
                        st.write(f"**Description:** {prop['description']}")

                    if prop.get('continuity_notes'):
                        st.info(f"📝 **Continuity:** {prop['continuity_notes']}")

                    col_a, col_b, col_c = st.columns(3)
                    with col_a:
                        if st.button("✏️ Edit", key=f"edit_{prop['id']}"):
                            st.session_state[f'editing_prop_{prop["id"]}'] = True
                            st.rerun()
                    with col_b:
                        new_status = st.selectbox(
                            "Quick Status Change",
                            ["needed", "sourced", "purchased", "rented", "ready", "on_set", "returned"],
                            key=f"status_{prop['id']}"
                        )
                        if st.button("Update", key=f"update_{prop['id']}"):
                            if api.update_prop_status(prop['id'], new_status):
                                show_success_clapper("Status Updated!")
                                st.rerun()
                    with col_c:
                        if st.button("🗑️ Delete", key=f"delete_{prop['id']}"):
                            if st.button("⚠️ Confirm Delete?", key=f"confirm_{prop['id']}"):
                                if api.delete_prop(prop['id']):
                                    show_success_clapper("Prop Deleted!")
                                    st.rerun()
        else:
            st.info("📦 No props yet. Add your first prop below!")

    with tab2:
        st.markdown("### ➕ Add New Prop")

        with st.form("add_prop_form"):
            col1, col2 = st.columns(2)

            with col1:
                name = st.text_input("Prop Name *", placeholder="e.g., Coffee Mug")
                category = st.selectbox("Category", [
                    "hand_prop", "set_dressing", "vehicle", "weapon",
                    "food", "document", "electronics", "furniture",
                    "costume_prop", "other"
                ], format_func=lambda x: x.replace('_', ' ').title())
                quantity = st.number_input("Quantity", min_value=1, value=1)
                status = st.selectbox("Status", [
                    "needed", "sourced", "purchased", "rented", "ready", "on_set", "returned"
                ])

            with col2:
                scenes = api.get_scenes(production['id'])
                scene_options = {f"Scene {s['scene_number']}": s['id'] for s in scenes}
                scene_options = {"None": None, **scene_options}

                selected_scene = st.selectbox("Scene (optional)", list(scene_options.keys()))
                scene_id = scene_options[selected_scene]

                source = st.text_input("Source", placeholder="e.g., Amazon, Prop Store")
                cost = st.number_input("Cost ($)", min_value=0.0, step=0.01)
                is_rented = st.checkbox("Rented Item")

                if is_rented:
                    rental_return_date = st.date_input("Return Date")
                else:
                    rental_return_date = None

            brand_model = st.text_input("Brand/Model", placeholder="e.g., Yeti 20oz")
            color = st.text_input("Color", placeholder="e.g., Black")
            size_dimensions = st.text_input("Size/Dimensions", placeholder="e.g., 8in x 3in")

            description = st.text_area("Description", placeholder="Detailed description...")
            continuity_notes = st.text_area("Continuity Notes",
                                            placeholder="Important continuity details...")

            hero_prop = st.checkbox("🌟 Hero Prop (Featured Item)")

            submitted = st.form_submit_button("➕ Add Prop", use_container_width=True)

            if submitted:
                if not name:
                    st.error("⚠️ Prop name is required")
                else:
                    prop_data = {
                        "production": production['id'],
                        "scene": scene_id,
                        "name": name,
                        "category": category,
                        "quantity": quantity,
                        "status": status,
                        "source": source,
                        "cost": cost if cost > 0 else None,
                        "is_rented": is_rented,
                        "rental_return_date": str(rental_return_date) if is_rented and rental_return_date else None,
                        "brand_model": brand_model,
                        "color": color,
                        "size_dimensions": size_dimensions,
                        "description": description,
                        "continuity_notes": continuity_notes,
                        "hero_prop": hero_prop
                    }

                    if api.create_prop(prop_data):
                        show_success_clapper("Prop Added Successfully!")
                        st.rerun()
                    else:
                        st.error("❌ Failed to add prop")


st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #888; font-size: 0.9rem;">
    💡 **Tip:** Props gives life to the moments !
    Make sure to treasure them...
</div>
""", unsafe_allow_html=True)
