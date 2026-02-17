"""
Logo component for ClapLog.
Uses base64 embedding - NO circular imports.
"""

import streamlit as st
import base64
from pathlib import Path


def _find_logo():
    """Search assets folder for any logo file. Returns Path or None."""
    assets_dir = Path(__file__).parent.parent / 'assets'

    logo_candidates = [
        'Logo.jpg',
        'Logo.png',
        'logo.jpg',
        'logo.png',
        'Logogif.gif',
        'logogif.gif',
        'Logo.gif',
        'logo.gif',
    ]

    for filename in logo_candidates:
        path = assets_dir / filename
        if path.exists():
            print(f"✅ Logo found: {path}")
            return path

    print("❌ No logo found in assets folder")
    return None


def _to_base64(logo_path):
    """Convert image file to base64 string. Returns (b64, mime_type) or (None, None)."""
    ext = logo_path.suffix.lower()
    mime_map = {
        '.png':  'image/png',
        '.jpg':  'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.gif':  'image/gif',
        '.webp': 'image/webp',
    }
    mime_type = mime_map.get(ext, 'image/png')

    try:
        with open(logo_path, 'rb') as f:
            b64 = base64.b64encode(f.read()).decode('utf-8')
        return b64, mime_type
    except Exception as e:
        print(f"❌ Could not read logo file: {e}")
        return None, None


def show_logo():
    """Show logo in sidebar using base64 embedding."""

    logo_path = _find_logo()
    b64, mime_type = _to_base64(logo_path) if logo_path else (None, None)

    if b64:
        st.sidebar.markdown(f"""
        <div style="
            text-align: center;
            padding: 1rem 0.5rem 1.5rem 0.5rem;
            border-bottom: 1px solid rgba(96,165,250,0.3);
            margin-bottom: 1rem;
        ">
            <img src="data:{mime_type};base64,{b64}" style="
                width: 80%;
                max-width: 180px;
                height: auto;
                display: block;
                margin: 0 auto;
                border-radius: 12px;
                box-shadow: 0 0 20px rgba(34,211,238,0.3);
            "/>
        </div>
        """, unsafe_allow_html=True)
    else:
        _text_logo_sidebar()


def show_logo_in_header():
    """Show logo in main header using base64 embedding."""

    logo_path = _find_logo()
    b64, mime_type = _to_base64(logo_path) if logo_path else (None, None)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if b64:
            st.markdown(f"""
            <div style="text-align:center; padding:2rem 0 1.5rem 0;">
                <img src="data:{mime_type};base64,{b64}" style="
                    width: 55%;
                    max-width: 220px;
                    height: auto;
                    display: block;
                    margin: 0 auto;
                    border-radius: 16px;
                    box-shadow:
                        0 0 40px rgba(34,211,238,0.5),
                        0 0 80px rgba(6,182,212,0.3),
                        0 8px 32px rgba(0,0,0,0.6);
                "/>
            </div>
            """, unsafe_allow_html=True)
        else:
            _text_logo_header()


def _text_logo_sidebar():
    """Fallback text logo for sidebar."""
    st.sidebar.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tangerine:wght@700&display=swap');
    </style>
    <div style="
        text-align: center;
        padding: 1.5rem 0.5rem;
        border-bottom: 1px solid rgba(96,165,250,0.3);
        margin-bottom: 1rem;
    ">
        <div style="
            font-family: 'Tangerine', cursive;
            font-size: 3.5rem;
            font-weight: 700;
            font-style: italic;
            color: #ffffff;
            text-shadow: 0 0 20px #22d3ee, 0 0 40px #06b6d4, 2px 2px 4px rgba(0,0,0,0.8);
            line-height: 1;
        ">ClapLog</div>
        <div style="
            font-family: 'Inter', sans-serif;
            font-size: 0.75rem;
            color: #22d3ee;
            text-transform: uppercase;
            letter-spacing: 2px;
            font-weight: 600;
            margin-top: 0.3rem;
        ">Film Production Tracker</div>
    </div>
    """, unsafe_allow_html=True)


def _text_logo_header():
    """Fallback text logo for header."""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tangerine:wght@700&display=swap');
    </style>
    <div style="text-align:center; padding:3rem 0 2rem 0;">
        <div style="
            font-family: 'Tangerine', cursive;
            font-size: 6rem;
            font-weight: 700;
            font-style: italic;
            color: #ffffff;
            text-shadow:
                0 0 30px #22d3ee,
                0 0 60px #06b6d4,
                0 0 90px #3b82f6,
                3px 3px 6px rgba(0,0,0,0.9);
            line-height: 1;
        ">ClapLog</div>
        <div style="
            font-family: 'Inter', sans-serif;
            font-size: 1.1rem;
            color: #22d3ee;
            text-transform: uppercase;
            letter-spacing: 4px;
            font-weight: 500;
            margin-top: 1rem;
        ">Track Your Vision · Frame by Frame</div>
    </div>
    """, unsafe_allow_html=True)