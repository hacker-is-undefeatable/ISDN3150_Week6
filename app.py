from pathlib import Path
from typing import Dict, List
import base64
import json

import streamlit as st
import streamlit.components.v1 as components


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
            header[data-testid="stHeader"] {
                display: none;
            }
            [data-testid="stToolbar"] {
                display: none;
            }
            [data-testid="stSidebar"], [data-testid="collapsedControl"] {
                display: none;
            }
            @media (min-width: calc(736px + 8rem)) {
                .st-emotion-cache-zy6yx3 {
                    padding-left: 0rem;
                    padding-right: 0rem;
                    padding: 0rem 0rem 0rem 0rem
                }
            }
            .main .block-container {
                max-width: 100%;
            }
            .scene-image-wrap {
                position: relative;
                width: 100%;
                height: 90vh;
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
                position: absolute;
                left: 1rem;
                right: 1rem;
                bottom: 1rem;
                margin: 0;
                padding: 1rem 1.2rem;
                background: rgba(0, 0, 0, 0.5);
                color: #f8f8f8;
                font-size: 1.04rem;
                line-height: 1.6;
                z-index: 5;
                border-radius: 16px;
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


def render_scene_with_typewriter(local_image: Path, text: str, speed_ms: int) -> None:
    image_uri = image_to_data_uri(local_image)
    text_js = json.dumps(text)
    scene_html = f"""
        <style>
            .scene-image-wrap {{
                position: relative;
                width: 100%;
                height: 90vh;
                border-radius: 18px;
                overflow: hidden;
                box-shadow: 0 18px 42px rgba(0, 0, 0, 0.24);
                background: #111;
            }}
            .scene-image-wrap img {{
                width: 100%;
                height: 100%;
                object-fit: cover;
                display: block;
            }}
            .scene-caption {{
                position: absolute;
                left: 1rem;
                right: 1rem;
                bottom: 1rem;
                margin: 0;
                padding: 1rem 1.2rem;
                background: rgba(0, 0, 0, 0.5);
                color: #f8f8f8;
                font-size: 1.04rem;
                line-height: 1.6;
                z-index: 5;
                border-radius: 16px;
                min-height: 3.2rem;
                white-space: pre-wrap;
            }}
        </style>
        <div class="scene-image-wrap">
            <img src="{image_uri}" alt="story scene" />
            <div class="scene-caption" id="scene-caption"></div>
        </div>
        <script>
            const fullText = {text_js};
            const target = document.getElementById("scene-caption");
            let i = 0;
            const timer = setInterval(() => {{
                target.textContent = fullText.slice(0, i);
                i += 1;
                if (i > fullText.length) {{
                    clearInterval(timer);
                }}
            }}, {speed_ms});
        </script>
    """
    components.html(
        scene_html,
        height=760,
        scrolling=False,
    )


typing_speed_ms = 12
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
    st.empty()
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

current_image = image_path(current_scene["image"])
if current_image.exists():
    render_scene_with_typewriter(current_image, current_scene["description"], typing_speed_ms)
else:
    st.warning(f"Image not found: {current_scene['image']}")
