"""
Animated components for ClapLog.
"""

import streamlit as st
import time


def show_clapperboard_animation(message="Action!"):
    """Show animated clapperboard for success messages."""

    st.markdown(f"""
    <style>
    @keyframes clapDown {{
        0% {{
            transform: rotateX(0deg) translateY(0);
        }}
        50% {{
            transform: rotateX(-15deg) translateY(-10px);
        }}
        100% {{
            transform: rotateX(0deg) translateY(0);
        }}
    }}

    @keyframes slideUp {{
        from {{
            opacity: 0;
            transform: translateY(50px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}

    .clapperboard-container {{
        text-align: center;
        padding: 3rem;
        animation: slideUp 0.5s ease-out;
    }}

    .clapper-top {{
        width: 300px;
        height: 60px;
        background: linear-gradient(135deg, #222 0%, #444 25%, #222 25%, #444 50%, #222 50%, #444 75%, #222 75%, #444 100%);
        background-size: 60px 60px;
        border: 4px solid #fff;
        border-bottom: none;
        border-radius: 10px 10px 0 0;
        margin: 0 auto;
        position: relative;
        animation: clapDown 0.6s ease-in-out 3;
        box-shadow: 0 -5px 15px rgba(0,0,0,0.5);
    }}

    .clapper-bottom {{
        width: 300px;
        height: 200px;
        background: linear-gradient(135deg, #000 0%, #1a1a1a 100%);
        border: 4px solid #fff;
        border-radius: 0 0 10px 10px;
        margin: 0 auto;
        padding: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.7);
    }}

    .clapper-text {{
        color: #fff;
        font-family: 'Courier New', monospace;
        font-size: 1.2rem;
        margin: 1rem 0;
        text-align: left;
    }}

    .clapper-message {{
        color: #daa520;
        font-size: 2rem;
        font-weight: bold;
        margin-top: 2rem;
        text-shadow: 0 0 10px rgba(218,165,32,0.5);
        animation: pulse 2s ease-in-out infinite;
    }}

    .clapper-hinges {{
        position: absolute;
        width: 8px;
        height: 8px;
        background: #888;
        border-radius: 50%;
        top: 50%;
        transform: translateY(-50%);
    }}

    .hinge-left {{ left: 10px; }}
    .hinge-right {{ right: 10px; }}
    </style>

    <div class="clapperboard-container">
        <div class="clapper-top">
            <div class="clapper-hinges hinge-left"></div>
            <div class="clapper-hinges hinge-right"></div>
        </div>
        <div class="clapper-bottom">
            <div class="clapper-text">PRODUCTION: ClapLog</div>
            <div class="clapper-text">DIRECTOR: You</div>
            <div class="clapper-text">SCENE: Success</div>
            <div class="clapper-text">TAKE: 1</div>
        </div>
        <div class="clapper-message">{message}</div>
    </div>
    """, unsafe_allow_html=True)

    time.sleep(3)


def show_success_clapper(message):
    """Quick success clapperboard animation."""

    placeholder = st.empty()

    with placeholder.container():
        st.markdown(f"""
        <style>
        @keyframes clapDown {{
            0% {{
                transform: rotateX(0deg);
            }}
            50% {{
                transform: rotateX(-20deg);
            }}
            100% {{
                transform: rotateX(0deg);
            }}
        }}

        @keyframes slideUp {{
            from {{
                opacity: 0;
                transform: translateY(30px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}

        @keyframes pulse {{
            0%, 100% {{
                opacity: 1;
            }}
            50% {{
                opacity: 0.7;
            }}
        }}
        </style>

        <div style="
            text-align: center;
            padding: 2rem;
            background: linear-gradient(135deg, rgba(218,165,32,0.15) 0%, rgba(139,0,0,0.15) 100%);
            border-radius: 15px;
            border: 3px solid #daa520;
            animation: slideUp 0.5s ease-out;
            margin: 1rem 0;
        ">
            <div style="font-size: 5rem; animation: clapDown 0.6s ease-in-out 2;">🎬</div>
            <h2 style="color: #daa520; margin: 1rem 0; font-family: 'Cinzel', serif; animation: pulse 1.5s ease-in-out infinite;">
                Action!
            </h2>
            <p style="color: #e8e8e8; font-size: 1.3rem; margin: 0.5rem 0;">{message}</p>
        </div>
        """, unsafe_allow_html=True)

    time.sleep(2.5)
    placeholder.empty()


def show_loading_film_reel(text="Processing..."):
    """Show film reel loading animation."""

    st.markdown(f"""
    <style>
    @keyframes spin {{
        from {{ transform: rotate(0deg); }}
        to {{ transform: rotate(360deg); }}
    }}

    @keyframes fadeIn {{
        from {{ opacity: 0; }}
        to {{ opacity: 1; }}
    }}
    </style>

    <div style="text-align: center; padding: 2rem; animation: fadeIn 0.5s ease-in;">
        <div style="
            font-size: 4rem;
            animation: spin 2s linear infinite;
            display: inline-block;
        ">🎞️</div>
        <p style="
            color: #daa520;
            font-size: 1.2rem;
            margin-top: 1rem;
            font-style: italic;
            animation: pulse 2s ease-in-out infinite;
        ">{text}</p>
    </div>
    """, unsafe_allow_html=True)


def show_countdown_animation(count=3):
    """Show a countdown animation (3, 2, 1, Action!)."""

    placeholder = st.empty()

    for i in range(count, 0, -1):
        with placeholder.container():
            st.markdown(f"""
            <div style="
                text-align: center;
                padding: 3rem;
                animation: pulse 0.5s ease-in-out;
            ">
                <div style="
                    font-size: 8rem;
                    color: #daa520;
                    font-weight: bold;
                    font-family: 'Cinzel', serif;
                ">{i}</div>
            </div>
            """, unsafe_allow_html=True)
        time.sleep(1)

    # Final "Action!"
    with placeholder.container():
        st.markdown("""
        <div style="
            text-align: center;
            padding: 3rem;
        ">
            <div style="font-size: 5rem;">🎬</div>
            <div style="
                font-size: 4rem;
                color: #daa520;
                font-weight: bold;
                font-family: 'Cinzel', serif;
            ">Action!</div>
        </div>
        """, unsafe_allow_html=True)

    time.sleep(1.5)
    placeholder.empty()


def show_typing_effect(text, delay=0.05):
    """Show text with typing effect."""

    placeholder = st.empty()
    displayed_text = ""

    for char in text:
        displayed_text += char
        placeholder.markdown(f"""
        <div style="
            color: #daa520;
            font-size: 1.5rem;
            font-family: 'Courier New', monospace;
            padding: 1rem;
        ">{displayed_text}<span style="animation: blink 1s infinite;">_</span></div>

        <style>
        @keyframes blink {{
            0%, 50% {{ opacity: 1; }}
            51%, 100% {{ opacity: 0; }}
        }}
        </style>
        """, unsafe_allow_html=True)
        time.sleep(delay)

    time.sleep(1)
    placeholder.empty()


def show_progress_animation(total_steps=5, step_names=None):
    """Show animated progress through steps."""

    if step_names is None:
        step_names = [f"Step {i + 1}" for i in range(total_steps)]

    progress_bar = st.progress(0)
    status_text = st.empty()

    for i, step_name in enumerate(step_names):
        progress = (i + 1) / total_steps
        progress_bar.progress(progress)

        status_text.markdown(f"""
        <div style="
            text-align: center;
            padding: 1rem;
            color: #daa520;
            font-size: 1.2rem;
        ">
            🎬 {step_name}...
        </div>
        """, unsafe_allow_html=True)

        time.sleep(0.5)

    status_text.success("✅ Complete!")
    time.sleep(1)
    progress_bar.empty()
    status_text.empty()


def show_confetti_animation():
    """Show confetti celebration."""

    st.balloons()

    st.markdown("""
    <div style="
        text-align: center;
        padding: 2rem;
        animation: slideUp 0.5s ease-out;
    ">
        <div style="font-size: 5rem;">🎉</div>
        <h2 style="
            color: #daa520;
            font-family: 'Cinzel', serif;
            margin: 1rem 0;
        ">Congratulations!</h2>
        <p style="color: #e8e8e8; font-size: 1.2rem;">That's a wrap!</p>
    </div>

    <style>
    @keyframes slideUp {{
        from {{
            opacity: 0;
            transform: translateY(30px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}
    </style>
    """, unsafe_allow_html=True)


def show_error_animation(message):
    """Show error animation."""

    st.markdown(f"""
    <style>
    @keyframes shake {{
        0%, 100% {{ transform: translateX(0); }}
        25% {{ transform: translateX(-10px); }}
        75% {{ transform: translateX(10px); }}
    }}

    @keyframes fadeIn {{
        from {{ opacity: 0; }}
        to {{ opacity: 1; }}
    }}
    </style>

    <div style="
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, rgba(231,76,60,0.15) 0%, rgba(192,57,43,0.15) 100%);
        border-radius: 15px;
        border: 3px solid #e74c3c;
        animation: fadeIn 0.5s ease-in;
        margin: 1rem 0;
    ">
        <div style="font-size: 4rem; animation: shake 0.5s ease-in-out;">⚠️</div>
        <h3 style="color: #e74c3c; margin: 1rem 0;">Error</h3>
        <p style="color: #e8e8e8; font-size: 1.1rem;">{message}</p>
    </div>
    """, unsafe_allow_html=True)


def show_camera_flash():
    """Show camera flash effect."""

    placeholder = st.empty()

    with placeholder.container():
        st.markdown("""
        <div style="
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: #fff;
            animation: flash 0.3s ease-out;
            pointer-events: none;
            z-index: 9999;
        "></div>

        <style>
        @keyframes flash {{
            0% {{ opacity: 0; }}
            50% {{ opacity: 0.8; }}
            100% {{ opacity: 0; }}
        }}
        </style>
        """, unsafe_allow_html=True)

    time.sleep(0.3)
    placeholder.empty()


def show_film_burn_transition():
    """Show old film burn transition effect."""

    placeholder = st.empty()

    with placeholder.container():
        st.markdown("""
        <div style="
            text-align: center;
            padding: 3rem;
        ">
            <div style="
                font-size: 6rem;
                animation: burn 2s ease-out;
            ">🔥</div>
            <p style="
                color: #daa520;
                font-size: 1.5rem;
                font-style: italic;
                animation: fadeOut 2s ease-out;
            ">Scene transition...</p>
        </div>

        <style>
        @keyframes burn {{
            0% {{ 
                opacity: 0;
                transform: scale(0.5);
            }}
            50% {{ 
                opacity: 1;
                transform: scale(1.2);
            }}
            100% {{ 
                opacity: 0;
                transform: scale(0.8);
            }}
        }}

        @keyframes fadeOut {{
            0% {{ opacity: 1; }}
            100% {{ opacity: 0; }}
        }}
        </style>
        """, unsafe_allow_html=True)

    time.sleep(2)
    placeholder.empty()
