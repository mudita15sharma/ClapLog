"""
Cast Members page - Manage actors and talent.
"""

import streamlit as st
import sys
from pathlib import Path

parent_dir = Path(__file__).parent.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

from api.client import APIClient
from styles.dark_theme import apply_dark_theme
from components.production_selector import show_production_selector
from components.animations import show_success_clapper
from components.visuals import show_page_quote, show_film_strip_divider
from components.logo import show_logo

st.set_page_config(
    page_title="Cast Members - ClapLog",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_dark_theme()


api = APIClient()
if 'token' in st.session_state and st.session_state.get('token'):
    api.token = st.session_state['token']

if not st.session_state.get('authenticated', False):
    st.warning("Please login first")
    if st.button("Go to Login"):
        st.switch_page("app.py")
    st.stop()

show_logo()
st.markdown("# 🎭 Cast Members")
show_page_quote("Cast")

production = show_production_selector(api, "Cast Members")

if not production:
    st.info("👆 Please select a production above to continue")
    st.stop()

st.markdown(f"### 🎭 Cast Members : **{production['title']}**")

tab1, tab2 = st.tabs(["🎭 All Cast", "➕ Add Cast Member"])

with tab1:
    st.subheader(f"Cast for: {production['title']}")

    col1, col2 = st.columns(2)
    with col1:
        filter_role = st.selectbox("Filter by Role Type", [
            "All", "lead", "supporting", "day_player", "extra", "stunt"
        ], format_func=lambda x: x.replace('_', ' ').title())

    with col2:
        search_query = st.text_input("🔍 Search by name or character", placeholder="Search...")

    cast_members = api.get_cast_members(production['id'])

    if filter_role != "All":
        cast_members = [c for c in cast_members if c.get('role_type') == filter_role]

    if search_query:
        search_lower = search_query.lower()
        cast_members = [
            c for c in cast_members
            if search_lower in c.get('name', '').lower()
               or search_lower in c.get('character_name', '').lower()
        ]

    if cast_members:
        st.write(f"**Total: {len(cast_members)} cast members**")

        for i in range(0, len(cast_members), 3):
            cols = st.columns(3)
            for j, col in enumerate(cols):
                if i + j < len(cast_members):
                    cast = cast_members[i + j]

                    with col:
                        role_icon = {
                            'lead': '⭐',
                            'supporting': '🎬',
                            'day_player': '🎭',
                            'extra': '👥',
                            'stunt': '🤸'
                        }.get(cast.get('role_type'), '🎭')

                        with st.container():
                            st.markdown(f"""
                            <div style="
                                background: linear-gradient(135deg, #1a1a1a 0%, #2a2a2a 100%);
                                padding: 1.5rem;
                                border-radius: 12px;
                                border: 2px solid #444;
                                margin: 0.5rem 0;
                                min-height: 250px;
                            ">
                                <div style="text-align: center; font-size: 3rem; margin-bottom: 0.5rem;">
                                    {role_icon}
                                </div>
                                <h3 style="color: #daa520; margin: 0.5rem 0; text-align: center;">
                                    {cast.get('name', 'Unknown')}
                                </h3>
                                <p style="color: #aaa; text-align: center; margin: 0.25rem 0;">
                                    as <strong>{cast.get('character_name', 'N/A')}</strong>
                                </p>
                                <p style="color: #888; text-align: center; font-size: 0.9rem; margin: 0.5rem 0;">
                                    {cast.get('role_type', '').replace('_', ' ').title()}
                                </p>
                            </div>
                            """, unsafe_allow_html=True)

                            with st.expander("📞 Contact & Details"):
                                if cast.get('contact_phone'):
                                    st.write(f"**Phone:** {cast['contact_phone']}")
                                if cast.get('contact_email'):
                                    st.write(f"**Email:** {cast['contact_email']}")
                                if cast.get('notes'):
                                    st.write(f"**Notes:** {cast['notes']}")

                                st.divider()

                                col_a, col_b = st.columns(2)
                                with col_a:
                                    if st.button("✏️ Edit", key=f"edit_cast_{cast['id']}", use_container_width=True):
                                        st.session_state[f'editing_cast_{cast["id"]}'] = True
                                        st.rerun()

                                with col_b:
                                    if st.button("🗑️ Delete", key=f"delete_cast_{cast['id']}", use_container_width=True,
                                                 type="secondary"):
                                        if st.session_state.get(f'confirm_delete_cast_{cast["id"]}'):
                                            if api.delete_cast_member(cast['id']):
                                                show_success_clapper("Cast Member Deleted!")
                                                st.rerun()
                                        else:
                                            st.session_state[f'confirm_delete_cast_{cast["id"]}'] = True
                                            st.warning("⚠️ Click again to confirm")
                                            st.rerun()


                            if st.session_state.get(f'editing_cast_{cast["id"]}'):
                                with st.form(f"edit_cast_form_{cast['id']}"):
                                    st.markdown("### ✏️ Edit Cast Member")

                                    edit_name = st.text_input("Name", value=cast.get('name', ''))
                                    edit_character = st.text_input("Character Name",
                                                                   value=cast.get('character_name', ''))
                                    edit_role_type = st.selectbox(
                                        "Role Type",
                                        ["lead", "supporting", "day_player", "extra", "stunt"],
                                        index=["lead", "supporting", "day_player", "extra", "stunt"].index(
                                            cast.get('role_type', 'supporting')),
                                        format_func=lambda x: x.replace('_', ' ').title()
                                    )
                                    edit_phone = st.text_input("Phone", value=cast.get('contact_phone', ''))
                                    edit_email = st.text_input("Email", value=cast.get('contact_email', ''))
                                    edit_notes = st.text_area("Notes", value=cast.get('notes', ''))

                                    col_s1, col_s2 = st.columns(2)
                                    with col_s1:
                                        save_btn = st.form_submit_button("💾 Save", use_container_width=True)
                                    with col_s2:
                                        cancel_btn = st.form_submit_button("❌ Cancel", use_container_width=True)

                                    if save_btn:
                                        update_data = {
                                            "production": production['id'],
                                            "name": edit_name,
                                            "character_name": edit_character,
                                            "role_type": edit_role_type,
                                            "contact_phone": edit_phone,
                                            "contact_email": edit_email,
                                            "notes": edit_notes
                                        }

                                        result = api.update_cast_member(cast['id'], update_data)
                                        if result:
                                            show_success_clapper("Cast Member Updated!")
                                            st.session_state[f'editing_cast_{cast["id"]}'] = False
                                            st.rerun()

                                    if cancel_btn:
                                        st.session_state[f'editing_cast_{cast["id"]}'] = False
                                        st.rerun()
    else:
        st.info("No cast members found. Add your first cast member!")

with tab2:
    st.subheader("Add New Cast Member")

    with st.form("create_cast_form"):
        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input("Actor Name *", placeholder="e.g., John Doe")
            character_name = st.text_input("Character Name *", placeholder="e.g., Detective Smith")
            role_type = st.selectbox("Role Type", [
                "lead", "supporting", "day_player", "extra", "stunt"
            ], format_func=lambda x: x.replace('_', ' ').title())

        with col2:
            contact_phone = st.text_input("Phone Number", placeholder="+1 (555) 123-4567")
            contact_email = st.text_input("Email", placeholder="actor@example.com")

        notes = st.text_area("Notes", placeholder="Additional information about the cast member...")

        submit = st.form_submit_button("🎭 Add Cast Member", use_container_width=True)

        if submit:
            if not name or not character_name:
                st.error("Name and character name are required!")
            else:
                data = {
                    "production": production['id'],
                    "name": name,
                    "character_name": character_name,
                    "role_type": role_type,
                    "contact_phone": contact_phone,
                    "contact_email": contact_email,
                    "notes": notes
                }

                with st.spinner("Adding Cast Member..."):
                    result = api.create_cast_member(data)

                if result:
                    show_success_clapper(f"{name} Added to Cast!")
                    st.success(f"✅ Cast Member Added!")
                    st.rerun()
                else:
                    st.error("❌ Failed to create call sheet. Please try again.")

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #888; font-size: 0.9rem;">
    💡 **Tip:**Cast Members have tight schedule !
    Make sure you book them early!
</div>
""", unsafe_allow_html=True)