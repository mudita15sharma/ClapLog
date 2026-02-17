"""
Production selector component for ClapLog.
Shows a dropdown to select active production.
"""

import streamlit as st


def show_production_selector(api , page_title=None):
    """
    Display production selector dropdown.
    Returns the selected production or None.

    Args:
        api: APIClient instance

    Returns:
        dict: Selected production data or None
    """

    productions = api.get_productions()

    if not productions:
        st.warning("⚠️ No productions found. Please create a production first.")
        if st.button("➕ Create Your First Production", type="primary"):
            st.switch_page("pages/Productions.py")
        return None

    prod_options = {p['title']: p for p in productions}

    current_prod = st.session_state.get('selected_production')

    if current_prod and current_prod['title'] in prod_options:
        default_index = list(prod_options.keys()).index(current_prod['title'])
    else:
        default_index = 0

    selected_title = st.selectbox(
        "🎬 Select Production",
        options=list(prod_options.keys()),
        index=default_index,
        key="production_selector"
    )

    new_prod = prod_options[selected_title]
    if not current_prod or current_prod['id'] != new_prod['id']:
        st.session_state.selected_production = new_prod
        st.rerun()

    return new_prod


def get_selected_production():
    """
    Get the currently selected production from session state.

    Returns:
        dict: Selected production data or None
    """
    return st.session_state.get('selected_production')


def require_production(api):
    """
    Require a production to be selected. If not, show selector and stop execution.

    Args:
        api: APIClient instance

    Returns:
        dict: Selected production data
    """
    prod = get_selected_production()

    if not prod:
        st.warning("⚠️ Please select a production first")
        show_production_selector(api)
        st.stop()

    return prod