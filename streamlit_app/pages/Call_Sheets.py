"""
Call Sheets page - Manage daily shooting schedules.

CHANGES MADE:
1. Fixed import order (imports before st.set_page_config)
2. Added missing imports (show_page_quote, show_film_strip_divider, show_production_selector)
3. Moved API initialization to correct position
4. Added production selector
5. Added success animations
6. Fixed page flow
"""

import streamlit as st
import sys
from pathlib import Path
from datetime import time

from streamlit_app.components.logo import show_logo

parent_dir = Path(__file__).parent.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

from api.client import APIClient
from styles.dark_theme import apply_dark_theme
from components.visuals import show_film_strip_divider, show_page_quote
from components.animations import show_success_clapper
from components.production_selector import show_production_selector


st.set_page_config(
    page_title="Call Sheets - ClapLog",
    page_icon="📅",
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

st.markdown("# 📅 Call Sheets")
show_page_quote("Call Sheets")

production = show_production_selector(api)

if not production:
    st.info("👆 Please select a production above to continue")
    st.stop()

st.markdown(f"### 📅 Call Sheets for: **{production['title']}**")

tab1, tab2 = st.tabs(["📅 All Call Sheets", "➕ Create Call Sheet"])

with tab1:
    st.markdown("### 📋 All Call Sheets")

    call_sheets = api.get_call_sheets(production['id'])

    if call_sheets:
        st.write(f"**Total: {len(call_sheets)} call sheets**")

        for cs in call_sheets:
            status_color = {
                'draft': '🟡',
                'published': '🟢',
                'in_progress': '🔵',
                'wrapped': '⚫',
                'cancelled': '🔴'
            }.get(cs.get('status', ''), '⚪')

            with st.expander(
                    f"{status_color} {cs.get('shoot_date', 'N/A')} - Call: {cs.get('call_time', 'N/A')}",
                    expanded=False
            ):
                col1, col2 = st.columns(2)

                with col1:
                    st.write(f"**📅 Shoot Date:** {cs.get('shoot_date', 'N/A')}")
                    st.write(f"**🕐 Call Time:** {cs.get('call_time', 'N/A')}")
                    st.write(f"**📊 Status:** {cs.get('status', '').replace('_', ' ').title()}")
                    st.write(f"**🎬 Day Number:** {cs.get('day_number') or 'N/A'}")

                with col2:
                    st.write(f"**👷 Crew Call:** {cs.get('crew_call_time') or 'N/A'}")
                    st.write(f"**🌅 Est. Wrap:** {cs.get('wrap_time_estimate') or 'N/A'}")
                    st.write(f"**🎞️ Scenes:** {cs.get('scene_count', 0)}")

                if cs.get('location_address'):
                    st.write(f"**📍 Location:**")
                    st.info(cs['location_address'])

                if cs.get('parking_info'):
                    st.write(f"**🅿️ Parking:**")
                    st.info(cs['parking_info'])

                col_a, col_b = st.columns(2)
                with col_a:
                    if cs.get('weather_forecast'):
                        st.write(f"**🌤️ Weather:** {cs['weather_forecast']}")
                    if cs.get('sunrise_time'):
                        st.write(f"**🌅 Sunrise:** {cs['sunrise_time']}")
                with col_b:
                    if cs.get('sunset_time'):
                        st.write(f"**🌇 Sunset:** {cs['sunset_time']}")
                    if cs.get('nearest_hospital'):
                        st.write(f"**🏥 Hospital:** {cs['nearest_hospital']}")

                if cs.get('safety_notes'):
                    st.warning(f"⚠️ **Safety:** {cs['safety_notes']}")

                if cs.get('general_notes'):
                    st.write(f"**📝 Notes:**")
                    st.info(cs['general_notes'])

                col_x, col_y, col_z = st.columns(3)
                with col_x:
                    if st.button("✏️ Edit", key=f"edit_{cs['id']}"):
                        st.info("Edit functionality coming soon!")
                with col_y:
                    if st.button("📄 Export PDF", key=f"export_{cs['id']}"):
                        st.info("PDF export coming soon!")
                with col_z:
                    if st.button("🗑️ Delete", key=f"delete_{cs['id']}"):
                        st.warning("Delete functionality coming soon!")
    else:
        st.info("📋 No call sheets yet. Create your first call sheet below!")


with tab2:
    st.markdown("### ➕ Create New Call Sheet")

    with st.form("create_call_sheet_form"):
        col1, col2 = st.columns(2)

        with col1:
            shoot_date = st.date_input("📅 Shoot Date *", help="Date of the shoot")
            day_number = st.number_input(
                "🎬 Day Number",
                min_value=1,
                value=1,
                help="Which day of production this is"
            )
            call_time = st.time_input(
                "🕐 General Call Time *",
                value=time(7, 0),
                help="When everyone should arrive"
            )
            crew_call_time = st.time_input(
                "👷 Crew Call Time",
                value=time(6, 30),
                help="When crew should arrive (usually earlier)"
            )

        with col2:
            wrap_time_estimate = st.time_input(
                "🌅 Estimated Wrap Time",
                value=time(18, 0),
                help="When you expect to finish"
            )
            status = st.selectbox(
                "📊 Status",
                ["draft", "published", "in_progress", "wrapped", "cancelled"],
                format_func=lambda x: x.replace('_', ' ').title()
            )

        st.markdown("#### 📍 Location Information")
        location_address = st.text_area(
            "Location Address",
            placeholder="123 Main St, Los Angeles, CA 90001\n\nDirections: Take Highway 101 to...",
            help="Full address with directions"
        )
        parking_info = st.text_area(
            "Parking Information",
            placeholder="Park in the north lot. Overflow parking available on Main Street.",
            help="Where cast and crew should park"
        )

        st.markdown("#### 🌤️ Weather & Timing")
        col_a, col_b = st.columns(2)

        with col_a:
            weather_forecast = st.text_input(
                "Weather Forecast",
                placeholder="Sunny, 75°F, light breeze"
            )
            sunrise_time = st.time_input(
                "🌅 Sunrise Time",
                value=time(6, 30)
            )

        with col_b:
            sunset_time = st.time_input(
                "🌇 Sunset Time",
                value=time(19, 0)
            )
            nearest_hospital = st.text_input(
                "🏥 Nearest Hospital",
                placeholder="St. Mary's Hospital - 456 Oak Ave (2 miles north)"
            )

        st.markdown("#### 📝 Notes")
        safety_notes = st.text_area(
            "⚠️ Safety Notes",
            placeholder="- Stunt coordinator on set\n- First aid kit in base camp\n- Watch for traffic on Main Street",
            help="Important safety information for the crew"
        )
        general_notes = st.text_area(
            "General Notes",
            placeholder="- Craft services at 8am, 12pm, 4pm\n- Special effects team arrives at noon\n- Director wants extra time for Scene 5",
            help="Any additional information for the day"
        )

        submitted = st.form_submit_button(
            "📅 Create Call Sheet",
            use_container_width=True,
            type="primary"
        )

        if submitted:
            if not shoot_date or not call_time:
                st.error("⚠️ Please fill in all required fields (marked with *)")
            else:
                data = {
                    "production": production['id'],
                    "shoot_date": str(shoot_date),
                    "day_number": day_number,
                    "call_time": str(call_time),
                    "crew_call_time": str(crew_call_time) if crew_call_time else None,
                    "wrap_time_estimate": str(wrap_time_estimate) if wrap_time_estimate else None,
                    "status": status,
                    "location_address": location_address,
                    "parking_info": parking_info,
                    "weather_forecast": weather_forecast,
                    "sunrise_time": str(sunrise_time) if sunrise_time else None,
                    "sunset_time": str(sunset_time) if sunset_time else None,
                    "nearest_hospital": nearest_hospital,
                    "safety_notes": safety_notes,
                    "general_notes": general_notes
                }


                with st.spinner("Creating call sheet..."):
                    result = api.create_call_sheet(data)

                if result:

                    show_success_clapper("Call Sheet Created!")
                    st.success(f"✅ Call sheet for {shoot_date} created successfully!")
                    st.balloons()
                    st.rerun()
                else:
                    st.error("❌ Failed to create call sheet. Please try again.")


st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #888; font-size: 0.9rem;">
    💡 **Tip:** Call sheets are typically distributed the day before shooting.
    Make sure to publish them early!
</div>
""", unsafe_allow_html=True)