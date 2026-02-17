"""
Enhanced dark cinema theme - Deep Ocean Professional Color Scheme
With high contrast text for dark blue backgrounds
"""

import streamlit as st
import base64
from pathlib import Path
import random


def set_background_image():
    assets_dir = Path(__file__).parent.parent / 'assets'
    images = list(assets_dir.glob('*.jpg')) + \
             list(assets_dir.glob('*.jpeg')) + \
             list(assets_dir.glob('*.png')) + \
             list(assets_dir.glob('*.webp'))

    images = [img for img in images if 'logo' not in img.name.lower()]

    if images:
        bg_image = random.choice(images)

        try:
            with open(bg_image, "rb") as f:
                data = f.read()
                b64 = base64.b64encode(data).decode()

            st.markdown(f"""
            <style>
            .stApp {{
                background-image: url("data:image/jpeg;base64,{b64}");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }}

            .stApp::before {{
                content: "";
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: linear-gradient(
                    180deg, 
                    rgba(10,14,20,0.97) 0%,
                    rgba(15,20,30,0.95) 100%
                opacity: 70%
                );
                z-index: -1;
                pointer-events: none;
            }}
            </style>
            """, unsafe_allow_html=True)
        except Exception as e:
            print(f"Failed to load background image: {e}")


def apply_dark_theme():

    set_background_image()

    css = """
    <style>
    
    @import url('https://fonts.googleapis.com/css2?family=Tangerine:wght@400;700&family=Dancing+Script:wght@400;500;600;700&family=Pacifico&family=Inter:wght@400;500;600;700&display=swap');

    :root {
        --primary-color: #60a5fa;          
        --primary-hover: #93c5fd;        

        --background-color: rgba(10,14,20,0.95);
        --secondary-bg: rgba(21,27,36,0.95);
        --card-bg: rgba(30,41,54,0.95);

        --text-color: #ffffff;            
        --text-secondary: #e2e8f0;       

        --accent-color: #22d3ee;           
        --accent-glow: #67e8f9;            
        --accent-dark: #06b6d4;            

        --border-color: rgba(96, 165, 250, 0.3);
        --success-color: #34d399;          
        --error-color: #f87171;          
        --warning-color: #fbbf24;        
        --hover-bg: rgba(96, 165, 250, 0.15);

        --font-script-primary: 'Tangerine', cursive;
        --font-script-secondary: 'Dancing Script', cursive;
        --font-script-alt: 'Pacifico', cursive;
        --font-body: 'Inter', sans-serif;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @keyframes slideIn {
        from { transform: translateX(-20px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }

    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.8; }
    }

    @keyframes glow {
        0%, 100% { 
            text-shadow: 0 0 10px var(--accent-color),
                         0 0 20px var(--accent-color),
                         0 0 30px var(--accent-glow);
        }
        50% { 
            text-shadow: 0 0 20px var(--accent-glow),
                         0 0 40px var(--accent-glow),
                         0 0 60px var(--accent-color);
        }
    }

    @keyframes shimmer {
        0% { background-position: -1000px 0; }
        100% { background-position: 1000px 0; }
    }

    .stApp {
        color: var(--text-color);
        font-family: var(--font-body);
        font-size: 26px !important;
        animation: fadeIn 0.5s ease-in;
    }


  
    h1 {
        font-size: 100px !important;
        font-family: 'Tangerine', cursive !important;
        font-weight: 700 !important;
        letter-spacing: 2px !important;
        color: #ffffff !important; 
        text-shadow: 
            0 0 20px var(--accent-glow),
            0 0 40px var(--accent-color),
            0 0 60px var(--accent-dark),
            2px 2px 4px rgba(0,0,0,0.8);
        animation: glow 3s ease-in-out infinite;
        margin: 2.5rem 0 !important;
        line-height: 1.1 !important;
        font-style: italic;
        -webkit-text-stroke: 0.5px rgba(34, 211, 238, 0.3);
    }

    h2 {
        font-size: 48px !important;
        font-family: 'Tangerine', cursive !important;
        font-weight: 700 !important;
        color: var(--accent-glow) !important;  
        letter-spacing: 1.5px !important;
        margin: 2rem 0 !important;
        text-shadow: 
            0 0 15px var(--accent-color),
            0 0 30px var(--accent-glow),
            2px 2px 4px rgba(0,0,0,0.8);
        line-height: 1.2 !important;
        font-style: italic;
        animation: glow 4s ease-in-out infinite;
    }

    h3 {
        font-size: 32px !important;
        font-family: 'Dancing Script', cursive !important;
        font-weight: 600 !important;
        color: #ffffff !important;  
        letter-spacing: 0.5px !important;
        margin: 1.5rem 0 !important;
        line-height: 1.4 !important;
        text-shadow: 
            0 0 10px var(--accent-color),
            2px 2px 4px rgba(0,0,0,0.8);
    }

    h4 {
        font-size: 26px !important;
        font-family: 'Dancing Script', cursive !important;
        font-weight: 500 !important;
        color: var(--accent-glow) !important;  
        margin: 1rem 0 !important;
        line-height: 1.4 !important;
        text-shadow: 0 0 10px var(--accent-color), 1px 1px 3px rgba(0,0,0,0.8);
    }

    p, div, span {
        font-size: 16px !important;
        line-height: 1.7 !important;
        color: #ffffff !important;  
        font-family: var(--font-body) !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
    }

    label {
        font-weight: 600 !important;
        color: var(--accent-glow) !important;  
        font-size: 16px !important;
        font-family: var(--font-body) !important;
        text-shadow: 0 0 10px var(--accent-color);
    }


    .stButton>button {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--accent-color) 100%);
        color: #000000 !important; 
        border: 2px solid var(--accent-glow);
        border-radius: 8px;
        padding: 14px 28px !important;
        font-size: 16px !important;
        font-weight: 700 !important;
        font-family: var(--font-body);
        letter-spacing: 0.5px !important;
        transition: all 0.3s ease;
        box-shadow: 0 0 20px var(--accent-color), 0 4px 15px rgba(34, 211, 238, 0.5);
    }

    .stButton>button:hover {
        background: linear-gradient(135deg, var(--accent-glow) 0%, var(--accent-color) 100%);
        transform: translateY(-2px);
        box-shadow: 0 0 30px var(--accent-glow), 0 6px 25px rgba(34, 211, 238, 0.7);
        border-color: #ffffff;
    }


    .stTextInput>div>div>input,
    .stSelectbox>div>div>select,
    .stTextArea>div>div>textarea,
    .stNumberInput>div>div>input,
    .stDateInput>div>div>input,
    .stTimeInput>div>div>input {
        background-color: rgba(20, 30, 50, 0.9) !important;
        color: #ffffff !important;  
        border: 2px solid var(--primary-color) !important;
        border-radius: 8px !important;
        transition: all 0.3s ease !important;
        font-family: var(--font-body) !important;
        font-size: 16px !important;
        font-weight: 400 !important;
        padding: 14px 18px !important;
    }

    .stTextInput>div>div>input:focus,
    .stSelectbox>div>div>select:focus,
    .stTextArea>div>div>textarea:focus,
    .stNumberInput>div>div>input:focus {
        border-color: var(--accent-glow) !important;
        box-shadow: 0 0 0 3px rgba(34, 211, 238, 0.3), 0 0 20px var(--accent-color) !important;
        background-color: rgba(30, 45, 70, 0.9) !important;
    }

    [data-testid="stMetricValue"] {
        font-size: 40px !important;
        font-weight: 700 !important;
        font-family: var(--font-body) !important;
        color: var(--accent-glow) !important;  
        text-shadow: 0 0 20px var(--accent-color), 0 0 40px var(--accent-glow);
        animation: pulse 3s ease-in-out infinite;
    }

    [data-testid="stMetricLabel"] {
        font-size: 15px !important;
        font-weight: 500 !important;
        font-family: var(--font-body) !important;
        color: #ffffff !important;  /* WHITE */
        text-transform: uppercase;
        letter-spacing: 1.5px;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
    }

    .stMetric {
        background: linear-gradient(135deg, rgba(30,41,54,0.95) 0%, rgba(21,27,36,0.95) 100%);
        padding: 28px;
        border-radius: 12px;
        border: 2px solid var(--primary-color);
        border-left: 5px solid var(--accent-glow);
        box-shadow: 
            0 8px 20px rgba(0, 0, 0, 0.5),
            0 0 30px rgba(34, 211, 238, 0.3);
        transition: all 0.3s ease;
        animation: fadeIn 0.8s ease-out;
    }

    .stMetric:hover {
        transform: translateY(-5px);
        box-shadow: 
            0 12px 30px rgba(0, 0, 0, 0.6),
            0 0 40px rgba(34, 211, 238, 0.5);
        border-color: var(--accent-glow);
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(21,27,36,0.98) 0%, rgba(10,14,20,0.98) 100%);
        border-right: 2px solid var(--primary-color);
        box-shadow: 6px 0 20px rgba(0, 0, 0, 0.7);
    }

    [data-testid="stSidebar"] * {
        font-size: 16px !important;
        font-family: var(--font-body) !important;
        color: #ffffff !important;  
    }

    [data-testid="stSidebarNav"] a {
        font-size: 16px !important;
        font-weight: 500 !important;
        font-family: var(--font-body) !important;
        padding: 14px 18px !important;
        border-radius: 8px;
        transition: all 0.3s ease;
        border-left: 3px solid transparent;
        color: #ffffff !important;
    }

    [data-testid="stSidebarNav"] a:hover {
        background: var(--hover-bg);
        border-left-color: var(--accent-glow);
        box-shadow: 0 0 20px rgba(34, 211, 238, 0.3);
        color: var(--accent-glow) !important;
    }

    .streamlit-expanderHeader {
        background: linear-gradient(135deg, rgba(30,41,54,0.95) 0%, rgba(21,27,36,0.95) 100%) !important;
        border: 2px solid var(--primary-color) !important;
        border-radius: 12px !important;
        font-size: 18px !important;
        font-weight: 600 !important;
        font-family: var(--font-body) !important;
        padding: 18px 22px !important;
        transition: all 0.3s ease !important;
        color: #ffffff !important;  
        text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
    }

    .streamlit-expanderHeader:hover {
        border-color: var(--accent-glow) !important;
        background: linear-gradient(135deg, rgba(40,55,75,0.95) 0%, rgba(30,41,54,0.95) 100%) !important;
        box-shadow: 0 0 25px rgba(34, 211, 238, 0.4) !important;
        color: var(--accent-glow) !important;
    }

    .stSuccess {
        background: linear-gradient(135deg, rgba(52, 211, 153, 0.25) 0%, rgba(16, 185, 129, 0.15) 100%);
        border-left: 4px solid var(--success-color);
        border-radius: 8px;
        font-size: 16px !important;
        font-family: var(--font-body) !important;
        padding: 18px 22px !important;
        color: #ffffff !important;
    }

    .stError {
        background: linear-gradient(135deg, rgba(248, 113, 113, 0.25) 0%, rgba(239, 68, 68, 0.15) 100%);
        border-left: 4px solid var(--error-color);
        border-radius: 8px;
        font-size: 16px !important;
        font-family: var(--font-body) !important;
        padding: 18px 22px !important;
        color: #ffffff !important;
    }

    .stInfo {
        background: linear-gradient(135deg, rgba(103, 232, 249, 0.25) 0%, rgba(34, 211, 238, 0.15) 100%);
        border-left: 4px solid var(--accent-glow);
        border-radius: 8px;
        font-size: 16px !important;
        font-family: var(--font-body) !important;
        padding: 18px 22px !important;
        color: #ffffff !important;
    }

    .stWarning {
        background: linear-gradient(135deg, rgba(251, 191, 36, 0.25) 0%, rgba(245, 158, 11, 0.15) 100%);
        border-left: 4px solid var(--warning-color);
        border-radius: 8px;
        font-size: 16px !important;
        font-family: var(--font-body) !important;
        padding: 18px 22px !important;
        color: #ffffff !important;
    }

    .stTabs [data-baseweb="tab-list"] {
        background-color: rgba(21,27,36,0.95);
        border-radius: 12px 12px 0 0;
        padding: 10px;
        border: 2px solid var(--primary-color);
        border-bottom: none;
    }

    .stTabs [data-baseweb="tab"] {
        color: #ffffff !important;
        font-size: 16px !important;
        font-weight: 500;
        font-family: var(--font-body) !important;
        padding: 12px 24px;
        transition: all 0.3s ease;
        border-radius: 8px 8px 0 0;
    }

    .stTabs [data-baseweb="tab"]:hover {
        background-color: var(--hover-bg);
        color: var(--accent-glow) !important;
    }

    .stTabs [aria-selected="true"] {
        border-bottom: 4px solid var(--accent-glow);
        background: linear-gradient(180deg, rgba(40,55,75,0.9) 0%, transparent 100%);
        color: var(--accent-glow) !important;
        font-weight: 700;
        box-shadow: 0 0 20px rgba(34, 211, 238, 0.4);
    }


    .stProgress > div > div > div {
        background: linear-gradient(90deg, var(--accent-color) 0%, var(--accent-glow) 50%, #ffffff 100%) !important;
        animation: shimmer 2s linear infinite;
        background-size: 200% 100%;
        height: 8px !important;
        border-radius: 4px;
        box-shadow: 0 0 15px var(--accent-glow);
    }


    .stFormSubmitButton>button {
        width: 100%;
        background: linear-gradient(135deg, var(--accent-glow) 0%, var(--accent-color) 100%);
        color: #000000 !important; 
        font-weight: 700;
        font-size: 16px !important;
        font-family: var(--font-body) !important;
        padding: 14px 28px;
        border: 2px solid #ffffff;
        text-transform: uppercase;
        letter-spacing: 1px;
        border-radius: 8px;
        box-shadow: 0 0 30px var(--accent-glow), 0 6px 20px rgba(34, 211, 238, 0.5);
    }

    .stFormSubmitButton>button:hover {
        background: linear-gradient(135deg, #ffffff 0%, var(--accent-glow) 100%);
        box-shadow: 0 0 40px #ffffff, 0 8px 30px rgba(255, 255, 255, 0.6);
        transform: translateY(-2px);
    }

    ::-webkit-scrollbar {
        width: 14px;
        height: 14px;
    }

    ::-webkit-scrollbar-track {
        background: rgba(10,14,20,0.8);
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, var(--accent-glow) 0%, var(--accent-color) 100%);
        border-radius: 10px;
        border: 2px solid rgba(10,14,20,0.8);
        box-shadow: 0 0 10px var(--accent-glow);
    }

    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, #ffffff 0%, var(--accent-glow) 100%);
        box-shadow: 0 0 20px var(--accent-glow);
    }

    .dataframe {
        background-color: rgba(30,41,54,0.95) !important;
        color: #ffffff !important;
        border-radius: 12px !important;
        overflow: hidden !important;
        border: 2px solid var(--primary-color) !important;
    }

    .dataframe thead {
        background: rgba(21,27,36,0.95) !important;
    }

    .dataframe th {
        color: var(--accent-glow) !important;
        font-weight: 700 !important;
        font-family: var(--font-body) !important;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-size: 14px !important;
        text-shadow: 0 0 10px var(--accent-color);
    }

    .dataframe td {
        font-family: var(--font-body) !important;
        font-size: 16px !important;
        color: #ffffff !important;
    }

    .dataframe tbody tr:hover {
        background: var(--hover-bg) !important;
    }

    [data-baseweb="select"] > div {
        background-color: rgba(20, 30, 50, 0.9) !important;
        border: 2px solid var(--primary-color) !important;
        font-size: 16px !important;
        font-family: var(--font-body) !important;
        color: #ffffff !important;
    }

    [data-baseweb="select"] ul {
        background-color: rgba(20, 30, 50, 0.95) !important;
        border: 2px solid var(--accent-color) !important;
    }

    [data-baseweb="select"] li {
        font-size: 16px !important;
        font-family: var(--font-body) !important;
        padding: 14px 18px !important;
        color: #ffffff !important;
    }

    [data-baseweb="select"] li:hover {
        background-color: var(--hover-bg) !important;
        color: var(--accent-glow) !important;
    }

    </style>
    """

    st.markdown(css, unsafe_allow_html=True)