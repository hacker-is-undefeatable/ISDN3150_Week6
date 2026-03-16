from pathlib import Path
from typing import Dict, List
import base64
import time
from html import escape

import streamlit as st


st.set_page_config(
    page_title="The Stray Cat's Journey",
    page_icon="🐈",
    layout="wide",
    initial_sidebar_state="collapsed",
)


SCENES: List[Dict[str, str]] = [
    {
        "title": "Scene 1: Discovering the stray cat in the park",
        "image": "scene1.png",
        "description": (
            "On the way back from class, a university student notices a lonely orange cat near a park bench. "
            "The cat looks tired and scared, with no collar or owner in sight."
        ),
    },
    {
        "title": "Scene 2: Feeding the cat and gaining its trust",
        "image": "scene2.png",
        "description": (
            "The student buys cat food from a nearby convenience store and places it gently on the ground. "
            "After a few cautious moments, the cat comes closer and begins to trust the student."
        ),
    },
    {
        "title": "Scene 3: Searching around town for the owner",
        "image": "scene3.png",
        "description": (
            "With the cat following nearby, the student visits local streets and shops asking if anyone recognizes it. "
            "People offer clues, but no one knows exactly where the cat belongs."
        ),
    },
    {
        "title": "Scene 4: Putting up lost cat posters",
        "image": "scene4.png",
        "description": (
            "The student prints simple lost cat posters and hangs them on lamp posts and community boards. "
            "By evening, the message spreads across the neighborhood."
        ),
    },
    {
        "title": "Scene 5: Reuniting the cat with its owner",
        "image": "scene5.png",
        "description": (
            "An elderly woman sees a poster and contacts the student. "
            "When they meet, the orange cat runs toward her immediately, and they are joyfully reunited."
        ),
    },
    {
        "title": "Scene 6: Walking home at sunset",
        "image": "scene6.png",
        "description": (
            "After saying goodbye, the student walks home under a warm sunset sky. "
            "Feeling grateful and happy, they reflect on the kindness of helping someone in need."
        ),
    },
]


def image_path(filename: str) -> Path:
    return Path(__file__).parent / "assets" / "images" / filename


def inject_page_style() -> None:
    st.markdown(
        """
        <style>
            [data-testid="stSidebar"], [data-testid="collapsedControl"] {
                display: none;
            }
            .main .block-container {
                max-width: 100%;
                padding-top: 1.2rem;
                padding-left: 1rem;
                padding-right: 1rem;
                padding-bottom: 5.5rem;
            }
            .scene-title {
                margin-top: 0.3rem;
                margin-bottom: 0.6rem;
                font-size: 1.35rem;
                font-weight: 600;
            }
            .scene-image-wrap {
                width: 100%;
                height: 78vh;
                border-radius: 18px;
                overflow: hidden;
                box-shadow: 0 18px 42px rgba(0, 0, 0, 0.24);
                background: #111;
            }
            .scene-image-wrap img {
                width: 100%;
                height: 100%;
                object-fit: cover;
                display: block;
            }
            .scene-caption {
                position: fixed;
                left: 0;
                right: 0;
                bottom: 0;
                margin: 0;
                padding: 1rem 1.2rem;
                background: linear-gradient(0deg, rgba(0, 0, 0, 0.88) 0%, rgba(0, 0, 0, 0.55) 100%);
                color: #f8f8f8;
                font-size: 1.04rem;
                line-height: 1.6;
                z-index: 999;
                border-top: 1px solid rgba(255, 255, 255, 0.2);
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def image_to_data_uri(local_image: Path) -> str:
    suffix = local_image.suffix.lower().replace(".", "")
    if suffix == "jpg":
        suffix = "jpeg"
    b64_data = base64.b64encode(local_image.read_bytes()).decode("ascii")
    return f"data:image/{suffix};base64,{b64_data}"


def render_fullscreen_image(local_image: Path) -> None:
    image_uri = image_to_data_uri(local_image)
    st.markdown(
        f"""
        <div class="scene-image-wrap">
            <img src="{image_uri}" alt="story scene" />
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_typewriter_caption(text: str, speed_seconds: float) -> None:
    caption_placeholder = st.empty()
    for idx in range(1, len(text) + 1):
        current_text = escape(text[:idx])
        caption_placeholder.markdown(
            f"<div class='scene-caption'>{current_text}</div>",
            unsafe_allow_html=True,
        )
        time.sleep(speed_seconds)


typing_speed = 0.03
total_scenes = len(SCENES)

if "scene_number" not in st.session_state:
    st.session_state.scene_number = 1


def go_previous() -> None:
    st.session_state.scene_number = max(1, st.session_state.scene_number - 1)


def go_next() -> None:
    st.session_state.scene_number = min(total_scenes, st.session_state.scene_number + 1)


nav_prev_col, nav_mid_col, nav_next_col = st.columns([1, 2, 1])
with nav_prev_col:
    st.button(
        "Previous",
        use_container_width=True,
        disabled=st.session_state.scene_number <= 1,
        on_click=go_previous,
    )
with nav_mid_col:
    st.markdown("<div style='text-align:center; font-weight:600;'>Scene Navigation</div>", unsafe_allow_html=True)
with nav_next_col:
    st.button(
        "Next",
        use_container_width=True,
        disabled=st.session_state.scene_number >= total_scenes,
        on_click=go_next,
    )

inject_page_style()

current_scene = SCENES[st.session_state.scene_number - 1]
scene_number = st.session_state.scene_number

st.markdown(f"<div class='scene-title'>{current_scene['title']}</div>", unsafe_allow_html=True)

current_image = image_path(current_scene["image"])
if current_image.exists():
    render_fullscreen_image(current_image)
else:
    st.warning(f"Image not found: {current_scene['image']}")

render_typewriter_caption(current_scene["description"], typing_speed)
