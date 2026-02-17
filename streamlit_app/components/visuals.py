"""
Visual components and decorations for ClapLog.
"""

import streamlit as st
import random


def show_logo_with_image():
    """Display ClapLog logo with cinematic styling."""

    st.markdown("""
    <div style="text-align: center; padding: 3rem 0; position: relative;">
        <div style="
            background: linear-gradient(135deg, rgba(10,10,10,0.95) 0%, rgba(26,26,26,0.9) 100%);
            padding: 4rem;
            border-radius: 25px;
            border: 4px solid #daa520;
            box-shadow: 
                0 15px 50px rgba(0,0,0,0.7), 
                0 0 40px rgba(218,165,32,0.3),
                inset 0 1px 0 rgba(255,255,255,0.1);
            display: inline-block;
            position: relative;
        ">
            <div style="font-size: 6rem; margin-bottom: 1.5rem; animation: pulse 2s ease-in-out infinite;">🎬</div>
            <h1 style="
                font-family: 'Cinzel', serif; 
                font-size: 5rem; 
                margin: 0;
                background: linear-gradient(135deg, #ffd700 0%, #daa520 50%, #b8860b 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                text-shadow: 2px 2px 15px rgba(218,165,32,0.4);
                letter-spacing: 3px;
            ">
                ClapLog
            </h1>
            <p style="
                font-style: italic; 
                color: #daa520; 
                font-size: 1.8rem; 
                margin-top: 1.5rem;
                letter-spacing: 3px;
                text-shadow: 1px 1px 5px rgba(0,0,0,0.5);
            ">
                Track your vision, frame by frame
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)


def show_random_film_quote():
    """Display a random inspirational film quote."""

    quotes = [
        ("Every frame tells a story", "Unknown"),
        ("The best camera is the one you have with you", "Chase Jarvis"),
        ("Film is truth 24 times a second", "Jean-Luc Godard"),
        ("A film is never really good unless the camera is an eye in the head of a poet", "Orson Welles"),
        ("Cinema is a matter of what's in the frame and what's out", "Martin Scorsese"),
        ("In film, we sculpt with time and space", "Andrei Tarkovsky"),
        ("The task I'm trying to achieve is above all to make you see", "D.W. Griffith"),
        ("Movies are a complicated collision of literature, theatre, music and photography", "Sydney Pollack"),
        ("The screen is a magic medium", "Stanley Kubrick"),
        ("Filmmaking is a chance to live many lifetimes", "Robert Altman"),
        ("When given an opportunity, deliver excellence and never quit", "Robert Rodriguez"),
        ("Every great film should seem new every time you see it", "Roger Ebert"),
        ("The cinema is truth 24 frames per second", "Jean-Luc Godard"),
        ("You don't make a photograph just with a camera. You bring to the act of photography all the pictures you have seen", "Ansel Adams"),
        ("A good film is when the price of the dinner, the theatre admission and the babysitter were worth it", "Alfred Hitchcock"),
    ]

    quote, author = random.choice(quotes)

    st.markdown(f"""
    <div style="
        text-align: center; 
        padding: 2.5rem;
        margin: 3rem auto;
        max-width: 900px;
        background: linear-gradient(135deg, rgba(218,165,32,0.08) 0%, rgba(139,0,0,0.08) 100%);
        border-radius: 15px;
        border-left: 5px solid #daa520;
        border-right: 5px solid #daa520;
    ">
        <div style="font-size: 2.5rem; color: #daa520; margin-bottom: 1rem;">🎞️</div>
        <p style="
            font-size: 1.8rem; 
            color: #daa520; 
            font-style: italic;
            margin: 1rem 0;
            line-height: 1.6;
            font-weight: 300;
        ">
            "{quote}"
        </p>
        <p style="
            font-size: 1.3rem; 
            color: #888;
            margin-top: 0.5rem;
            font-weight: 500;
        ">
            — {author}
        </p>
    </div>
    """, unsafe_allow_html=True)


def show_film_strip_divider():
    """Display a film strip divider."""
    st.markdown("""
    <div style="text-align: center; margin: 3rem 0;">
        <div style="
            display: inline-block; 
            background: linear-gradient(90deg, transparent, #daa520, transparent); 
            height: 4px; 
            width: 85%;
        "></div>
        <div style="font-size: 2.5rem; margin: 1rem 0;">🎞️</div>
        <div style="
            display: inline-block; 
            background: linear-gradient(90deg, transparent, #daa520, transparent); 
            height: 4px; 
            width: 85%;
        "></div>
    </div>
    """, unsafe_allow_html=True)


def show_clapperboard(title, subtitle=""):
    """Display a clapperboard-style header."""
    st.markdown(f"""
    <div style="
        position: relative;
        padding: 2rem;
        background: linear-gradient(135deg, #1a1a1a 0%, #2a2a2a 100%);
        border: 3px solid #daa520;
        border-radius: 15px;
        margin: 2rem 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    ">
        <div style="
            position: absolute;
            top: -1.5rem;
            left: 2rem;
            background: var(--background-color);
            padding: 0 1rem;
            font-size: 3rem;
        ">🎬</div>
        <h2 style="
            margin: 0; 
            color: #daa520;
            font-family: 'Cinzel', serif;
            font-size: 2.5rem;
        ">{title}</h2>
        {f'<p style="margin: 1rem 0 0 0; color: #e8e8e8; font-size: 1.3rem; font-style: italic;">{subtitle}</p>' if subtitle else ''}
    </div>
    """, unsafe_allow_html=True)


def show_page_quote(page_name):
    """Show a contextual quote for specific pages."""

    page_quotes = {
        "Scenes": [
            ("A scene should be a story in itself", "Unknown"),
            ("Every scene must advance the plot or reveal character", "Robert McKee"),
            ("The screenplay is the most important element", "Alfred Hitchcock"),
        ],
        "Shots": [
            ("The camera is much more than a recording apparatus", "Stanley Kubrick"),
            ("Composition is the strongest way of seeing", "Edward Weston"),
            ("Every shot must be motivated", "Roger Deakins"),
        ],
        "Call Sheets": [
            ("Pre-production is where you win or lose the battle", "Unknown"),
            ("Organization is the key to efficiency", "Film Wisdom"),
            ("Proper planning prevents poor performance", "Unknown"),
        ],
        "Continuity": [
            ("Continuity is the magic that makes movies seamless", "Unknown"),
            ("The details make perfection, and perfection is not a detail", "Leonardo da Vinci"),
            ("God is in the details", "Ludwig Mies van der Rohe"),
        ],
        "Productions": [
            ("A film is a world unto itself", "Unknown"),
            ("Great films are made in pre-production", "Steven Spielberg"),
            ("The whole is greater than the sum of its parts", "Aristotle"),
        ],
        "Cast": [
            ("The right actor can make all the difference", "Unknown"),
            ("Casting is 90% of directing", "Martin Scorsese"),
            ("An actor is something less than a man, while an actress is something more than a woman", "Richard Burton"),
        ],
        "Props": [
            ("Props are the secret life of a film", "Unknown"),
            ("Every object tells a story", "Unknown"),
            ("The devil is in the details", "Unknown"),
        ],
        "Cast": [
            ("The right actor can make all the difference", "Unknown"),
            ("Casting is 90% of directing", "Martin Scorsese"),
        ],
    }

    quotes = page_quotes.get(page_name, [("Make every shot count", "Unknown")])
    quote, author = random.choice(quotes)

    st.markdown(f"""
    <div style="
        text-align: center;
        padding: 1.5rem;
        margin: 2rem 0;
        background: linear-gradient(135deg, rgba(139,0,0,0.1) 0%, rgba(218,165,32,0.1) 100%);
        border-radius: 10px;
        border-top: 2px solid #daa520;
        border-bottom: 2px solid #daa520;
    ">
        <p style="
            font-size: 1.4rem;
            color: #daa520;
            font-style: italic;
            margin: 0.5rem 0;
        ">"{quote}"</p>
        <p style="font-size: 1.1rem; color: #888; margin: 0.5rem 0;">— {author}</p>
    </div>
    """, unsafe_allow_html=True)


def show_production_card(production):
    """Display a production as a movie poster card."""
    completion = production.get('completion_percentage', 0)

    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #1a1a1a 0%, #2a2a2a 100%);
        border: 2px solid #444;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        transition: all 0.3s ease;
    " onmouseover="this.style.transform='translateY(-5px)'; this.style.boxShadow='0 8px 12px rgba(218,165,32,0.3)';" 
       onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 4px 6px rgba(0,0,0,0.3)';">
        <div style="display: flex; align-items: center; margin-bottom: 1rem;">
            <div style="font-size: 3rem; margin-right: 1rem;">🎬</div>
            <div>
                <h3 style="margin: 0; color: #daa520;">{production.get('title', 'Untitled')}</h3>
                <p style="margin: 0.25rem 0 0 0; color: #aaa;">
                    Director: {production.get('director', 'Unknown')}
                </p>
            </div>
        </div>
        <div style="background: #0a0a0a; border-radius: 6px; height: 8px; overflow: hidden; margin: 1rem 0;">
            <div style="
                background: linear-gradient(90deg, #8b0000 0%, #daa520 50%, #ffd700 100%);
                height: 100%;
                width: {completion}%;
                transition: width 0.5s ease;
            "></div>
        </div>
        <p style="text-align: right; margin: 0; color: #daa520; font-weight: bold;">
            {completion:.1f}% Complete
        </p>
    </div>
    """, unsafe_allow_html=True)


def show_loading_animation(text="Loading..."):
    """Display a film-themed loading animation."""
    st.markdown(f"""
    <div style="text-align: center; padding: 2rem;">
        <div style="font-size: 3rem; animation: pulse 1.5s ease-in-out infinite;">🎬</div>
        <p style="color: #daa520; font-style: italic; margin-top: 1rem;">{text}</p>
    </div>
    """, unsafe_allow_html=True)


def show_success_animation(text):
    """Display a success animation."""
    st.markdown(f"""
    <div style="text-align: center; padding: 1rem; animation: slideIn 0.5s ease-out;">
        <div style="font-size: 3rem;">🎉</div>
        <p style="color: #2ecc71; font-weight: bold; margin-top: 0.5rem;">{text}</p>
    </div>
    """, unsafe_allow_html=True)


def show_background_pattern():
    """Add subtle background pattern."""
    st.markdown("""
    <style>
    .stApp {
        background-image: 
            radial-gradient(circle at 20% 30%, rgba(218,165,32,0.05) 0%, transparent 50%),
            radial-gradient(circle at 80% 70%, rgba(139,0,0,0.05) 0%, transparent 50%);
    }
    </style>
    """, unsafe_allow_html=True)


def show_stat_card(icon, title, value, color="#daa520"):
    """Display a statistic card."""
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #1a1a1a 0%, #2a2a2a 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid {color};
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        margin: 0.5rem 0;
    ">
        <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">{icon}</div>
        <div style="color: #888; font-size: 0.9rem; margin-bottom: 0.25rem;">{title}</div>
        <div style="color: {color}; font-size: 2rem; font-weight: bold;">{value}</div>
    </div>
    """, unsafe_allow_html=True)


def show_error_message(title, message):
    """Display a cinematic error message."""
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, rgba(231,76,60,0.1) 0%, rgba(192,57,43,0.1) 100%);
        padding: 2rem;
        border-radius: 12px;
        border-left: 5px solid #e74c3c;
        margin: 1rem 0;
    ">
        <h3 style="color: #e74c3c; margin: 0 0 0.5rem 0;">⚠️ {title}</h3>
        <p style="color: #e8e8e8; margin: 0;">{message}</p>
    </div>
    """, unsafe_allow_html=True)


def show_info_box(title, message, icon="ℹ️"):
    """Display an info box."""
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, rgba(52,152,219,0.1) 0%, rgba(41,128,185,0.1) 100%);
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #3498db;
        margin: 1rem 0;
    ">
        <h4 style="color: #3498db; margin: 0 0 0.5rem 0;">{icon} {title}</h4>
        <p style="color: #e8e8e8; margin: 0; font-size: 1.1rem;">{message}</p>
    </div>
    """, unsafe_allow_html=True)

def show_countdown_timer(days_left, event_name="Shoot Day"):
    """Display a countdown timer."""
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #1a1a1a 0%, #2a2a2a 100%);
        padding: 2rem;
        border-radius: 15px;
        border: 3px solid #daa520;
        text-align: center;
        margin: 1rem 0;
    ">
        <div style="font-size: 4rem; color: #daa520; font-weight: bold;">{days_left}</div>
        <p style="color: #888; font-size: 1.2rem; margin: 0.5rem 0;">days until</p>
        <p style="color: #e8e8e8; font-size: 1.5rem; font-weight: bold; margin: 0;">{event_name}</p>
    </div>
    """, unsafe_allow_html=True)


def show_progress_ring(percentage, label="Progress"):
    """Display a circular progress indicator."""
    st.markdown(f"""
    <div style="
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #1a1a1a 0%, #2a2a2a 100%);
        border-radius: 15px;
        margin: 1rem 0;
    ">
        <div style="
            font-size: 4rem;
            font-weight: bold;
            background: linear-gradient(135deg, #ffd700 0%, #daa520 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        ">{percentage}%</div>
        <p style="color: #888; font-size: 1.2rem; margin-top: 0.5rem;">{label}</p>
    </div>
    """, unsafe_allow_html=True)

def show_background_pattern():
    """Add subtle background pattern."""
    st.markdown("""
    <style>
    .stApp {
        background-image: 
            radial-gradient(circle at 20% 30%, rgba(218,165,32,0.05) 0%, transparent 50%),
            radial-gradient(circle at 80% 70%, rgba(139,0,0,0.05) 0%, transparent 50%);
    }
    </style>
    """, unsafe_allow_html=True)
