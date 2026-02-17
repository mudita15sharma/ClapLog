"""
Main Streamlit app for ClapLog - Film Production Tracker
"""

import streamlit as st
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from api.client import APIClient
from components.visuals import (
    show_logo_with_image,
    show_random_film_quote,
    show_film_strip_divider
)
from components.animations import show_success_clapper
from components.logo import show_logo, show_logo_in_header
from styles.dark_theme import apply_dark_theme

st.set_page_config(
    page_title="ClapLog - Film Production Tracker",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_dark_theme()

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'token' not in st.session_state:
    st.session_state.token = None
if 'user' not in st.session_state:
    st.session_state.user = None

api = APIClient()


def login_page():

    query_params = st.query_params
    if 'verify_email' in query_params:
        token = query_params['verify_email']

        with st.spinner("Verifying your email..."):
            result = api.verify_email(token)

        if result:
            st.success("✅ Email verified successfully! You can now log in.")
            st.balloons()
            st.query_params.clear()
        else:
            st.error("❌ Invalid or expired verification token.")

    tab1, tab2 = st.tabs(["🎬 Login", "📝 Register"])

    with tab1:
        st.markdown("### 🎬 Login to ClapLog")

        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")

            col1, col2 = st.columns(2)
            with col1:
                submit = st.form_submit_button("🎬 Action!", use_container_width=True, type="primary")
            with col2:
                if st.form_submit_button("🔄 Reset Form", use_container_width=True):
                    st.rerun()

            if submit:
                if not username or not password:
                    st.error("⚠️ Please enter both username and password")
                else:
                    with st.spinner("Logging in..."):
                        token = api.login(username, password)

                    if token:
                        st.session_state.authenticated = True
                        st.session_state.token = token
                        api.token = token

                        user = api.get_current_user()
                        if user:
                            st.session_state.user = user

                        show_success_clapper("Login Successful!")
                        st.success(f"✅ Welcome back, {username}!")
                        st.rerun()

        with st.form("resend_verification_form"):
            st.markdown("#### 📧 Didn't receive verification email?")
            email = st.text_input("Email Address", placeholder="your.email@example.com")
            resend = st.form_submit_button("📧 Resend Verification Email", use_container_width=True)

            if resend:
                if not email:
                    st.error("⚠️ Please enter your email address")
                else:
                    with st.spinner("Sending verification email..."):
                        if api.resend_verification(email):
                            st.success("✅ Verification email sent! Check your inbox.")
                        else:
                            st.error("❌ Failed to send verification email.")

        st.markdown("---")
        col_a, col_b, col_c = st.columns(3)

        with col_a:
            st.markdown("**📖 About ClapLog**")
            st.markdown("Professional film production tracking for modern filmmakers.")

        with col_b:
            st.markdown("**✨ Features**")
            st.markdown(
                "• Scene Management\n"
                "• Shot Tracking\n"
                "• Call Sheets\n"
                "• Continuity Notes"
                "• Production\n"
                "• Props management\n"
                "• Cast Members Record \n")

        with col_c:
            st.markdown("**❓ Need Help?**")
            st.markdown("Contact support at ClapLog.com")

    with tab2:
        st.markdown("### 📝 Join the Production")

        with st.form("register_form"):
            col1, col2 = st.columns(2)

            with col1:
                reg_username = st.text_input("Username *", placeholder="Choose a username")
                reg_email = st.text_input("Email *", placeholder="your.email@example.com")
                reg_first_name = st.text_input("First Name", placeholder="Your first name")

            with col2:
                reg_password = st.text_input("Password *", type="password", placeholder="Choose a strong password")
                reg_password2 = st.text_input("Confirm Password *", type="password", placeholder="Confirm your password")
                reg_last_name = st.text_input("Last Name", placeholder="Your last name")

            reg_role = st.selectbox("Role", [
                "director",
                "producer",
                "cinematographer",
                "editor",
                "crew",
                "other"
            ], format_func=lambda x: x.title())

            submit_register = st.form_submit_button("🎬 Join Production", use_container_width=True, type="primary")

            if submit_register:
                if not reg_username or not reg_email or not reg_password or not reg_password2:
                    st.error("⚠️ Please fill in all required fields (marked with *)")
                elif reg_password != reg_password2:
                    st.error("⚠️ Passwords do not match")
                elif len(reg_password) < 8:
                    st.error("⚠️ Password must be at least 8 characters long")
                else:
                    data = {
                        "username": reg_username,
                        "email": reg_email,
                        "password": reg_password,
                        "password2": reg_password2,
                        "first_name": reg_first_name or "",
                        "last_name": reg_last_name or "",
                        "role": reg_role
                    }

                    with st.spinner("Creating your account..."):
                        result = api.register(data)

                    if result:
                        show_success_clapper("Account Created!")
                        st.success("✅ Account created successfully!")
                        st.info("📧 Please check your email to verify your account before logging in.")
                        st.balloons()
                    else:
                        st.error("❌ Registration failed. Username or email may already be in use.")


def dashboard_page():
    show_logo()

    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tangerine:wght@700&family=Dancing+Script:wght@600&family=Inter:wght@400;500;600;700&display=swap');
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <p style="font-family:'Tangerine',cursive;font-size:5rem;font-weight:700;
        font-style:italic;color:#ffffff;line-height:1;margin-bottom:0;
        text-shadow:0 0 30px #22d3ee,0 0 60px #06b6d4,3px 3px 6px rgba(0,0,0,0.9);">
        ClapLog <span style="font-family:'Inter',sans-serif;font-size:1rem;
        color:#22d3ee;letter-spacing:3px;">PRO</span>
    </p>
    <p style="color:rgba(226,232,240,0.6);font-size:1rem;margin-top:0;">
        Professional Film Production Tracking
    </p>
    """, unsafe_allow_html=True)

    show_random_film_quote()

    user     = st.session_state.get('user', {})
    username = user.get('username', 'Filmmaker')
    st.info(f"🎬 Welcome back, **{username}**!")

    api.token = st.session_state.get('token')
    with st.spinner("Loading your productions..."):
        productions = api.get_productions() or []

    st.markdown("### 📊 Production Overview")

    total_productions  = len(productions)
    active_productions = len([p for p in productions
                               if p.get('status') in ('in_production', 'filming')])
    total_scenes       = sum(p.get('scene_count', 0)           for p in productions)
    total_shots        = sum(p.get('shot_count',  0)           for p in productions)
    done_scenes        = sum(p.get('completed_scene_count', 0) for p in productions)
    completion_pct     = f"{int((done_scenes / total_scenes) * 100)}%" if total_scenes > 0 else "—"

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("🎬 Productions",  total_productions,
                  delta=f"{active_productions} active" if active_productions else None)
    with m2:
        st.metric("📋 Total Scenes", total_scenes)
    with m3:
        st.metric("📷 Total Shots",  total_shots)
    with m4:
        st.metric("✅ Completion",   completion_pct,
                  delta=f"{done_scenes}/{total_scenes} done" if total_scenes > 0 else None)

    st.divider()

    st.markdown("### 🎬 Active Productions")
    st.caption("All your productions at a glance")

    STATUS_EMOJI = {
        'in_production':   '🎥 Filming',
        'filming':         '🎥 Filming',
        'pre_production':  '🔵 Pre-Production',
        'post_production': '🟡 Post-Production',
        'completed':       '✅ Completed',
        'development':     '💡 Development',
        'on_hold':         '⏸ On Hold',
    }

    if not productions:
        st.info("📋 No productions yet. Create your first one!")
        if st.button("➕ Create First Production", use_container_width=True):
            st.switch_page("pages/Productions.py")
    else:
        for i in range(0, len(productions), 2):
            col_l, col_r = st.columns(2)

            for col, prod in zip([col_l, col_r], productions[i:i+2]):
                sc       = prod.get('scene_count', 0)
                shots    = prod.get('shot_count',  0)
                done     = prod.get('completed_scene_count', 0)
                progress = (done / sc) if sc > 0 else 0.0
                pct      = int(progress * 100)
                title    = prod.get('title', 'Untitled')
                desc     = (prod.get('description', '') or '').strip()
                status   = prod.get('status', 'development')
                label    = STATUS_EMOJI.get(status, status.replace('_', ' ').title())
                start    = prod.get('start_date', '') or ''
                end      = prod.get('end_date',   '') or ''
                dates    = f"{start} → {end}" if start and end else start or 'No date set'

                with col:
                    with st.container(border=True):
                        t_col, b_col = st.columns([3, 1])
                        with t_col:
                            st.markdown(f"**{title}**")
                        with b_col:
                            st.caption(label)

                        if desc:
                            st.caption(desc[:100])


                        s1, s2, s3 = st.columns(3)
                        with s1:
                            st.metric("Scenes", f"{done}/{sc}", label_visibility="collapsed")
                            st.caption(f"**Scenes:** {done}/{sc}")
                        with s2:
                            st.caption(f"**Shots:** {shots}")
                        with s3:
                            st.caption(f"**Progress:** {pct}%")

                        st.caption(f"📅 {dates}")

                        st.progress(progress)

    st.divider()

    st.markdown("### ⚡ Quick Actions")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if st.button("➕ New Production",    use_container_width=True):
            st.switch_page("pages/Productions.py")
    with c2:
        if st.button("📋 Add Scene",         use_container_width=True):
            st.switch_page("pages/Scenes.py")
    with c3:
        if st.button("📅 Create Call Sheet", use_container_width=True):
            st.switch_page("pages/Call_Sheets.py")
    with c4:
        if st.button("📷 Add Shot",          use_container_width=True):
            st.switch_page("pages/Shots.py")

    st.divider()

    col_a, col_b = st.columns([2, 1])

    with col_a:
        st.markdown("### 📊 Production Summary")

        if productions:

            for prod in productions[:5]:
                sc    = prod.get('scene_count', 0)
                done  = prod.get('completed_scene_count', 0)
                shots = prod.get('shot_count', 0)
                pct   = int((done / sc) * 100) if sc > 0 else 0
                stat  = STATUS_EMOJI.get(
                    prod.get('status', 'development'),
                    prod.get('status', '').replace('_', ' ').title()
                )
                with st.container(border=True):
                    left, right = st.columns([4, 1])
                    with left:
                        st.markdown(f"**{prod.get('title','Untitled')}**")
                        st.caption(f"{done}/{sc} scenes · {shots} shots · {stat}")
                    with right:
                        st.markdown(f"### {pct}%")
                    st.progress((done / sc) if sc > 0 else 0.0)
        else:
            st.info("No productions yet.")

    with col_b:
        st.markdown("### 🎯 At a Glance")

        if productions:
            latest = max(productions, key=lambda p: p.get('scene_count', 0))
            sc     = latest.get('scene_count', 0)
            done   = latest.get('completed_scene_count', 0)
            rem    = sc - done
            prog   = (done / sc) if sc > 0 else 0.0

            with st.container(border=True):
                st.markdown(f"**🎬 {latest.get('title', 'N/A')}**")
                st.divider()
                g1, g2 = st.columns(2)
                with g1:
                    st.metric("Total",     sc)
                    st.metric("Remaining", rem)
                with g2:
                    st.metric("Done",  done)
                    st.metric("Shots", latest.get('shot_count', 0))
                st.progress(prog)
        else:
            st.info("Create a production to see stats here!")

    st.divider()

    if st.button("🚪 Logout", type="secondary"):
        for key in ['authenticated', 'token', 'user', 'selected_production']:
            st.session_state[key] = None
        st.session_state.authenticated = False
        st.rerun()

if not st.session_state.get('authenticated'):
    show_logo_in_header()
    login_page()
else:
    dashboard_page()