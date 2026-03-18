from pathlib import Path
import base64
import time
import html

import streamlit as st


st.set_page_config(
    page_title="The Stray Cat's Journey",
    page_icon="🐈",
    layout="wide",
    initial_sidebar_state="collapsed",
)


SCENE_IMAGES = {
    1: "1.jpeg",
    2: "2.jpeg",
    3: "3.jpeg",
    4: "4.jpeg",
    5: "5.jpeg",
    6: "6.jpeg",
    7: "7.jpeg",
    8: "8.jpeg",
    9: "9.jpeg",
}

NEXT_SCENE = {
    1: 2,
    2: 3,
    4: 7,
    5: 8,
    6: 9,
}

PREV_SCENE = {
    2: 1,
    3: 2,
    4: 3,
    5: 3,
    6: 3,
    7: 4,
    8: 5,
    9: 6,
}

ENDING_SCENES = {5, 7, 9}

NARRATIONS = {
    1: [
        "The afternoon was quiet, the kind of quiet that makes small things stand out.",
        "Under the bench, a pair of cautious eyes watched her every move.",
        "She had not planned to stop... but something about the little cat made her stay.",
    ],
    2: [
        "She gently placed the food down, careful not to scare it away.",
        "The cat hesitated, as if deciding whether to trust her.",
        "Moments later, it took a small step forward - and then another.",
    ],
    3: [
        "Now that it was no longer alone, the question became hers to answer.",
        "She looked at the cat, wondering where it truly belonged.",
        "Helping it meant making a choice... and every choice felt important.",
    ],
    4: [
        "She decided to search for its owner the old-fashioned way.",
        "Each poster carried a small hope - that someone, somewhere, was looking for this cat.",
        "The wind brushed against the paper, as if carrying her message through the streets.",
    ],
    5: [
        "At last, someone recognized the cat.",
        "The moment they reunited, everything felt right again.",
        "She smiled quietly, knowing she had helped something find its way home.",
    ],
    6: [
        "Maybe someone nearby had seen this cat before.",
        "She asked around, one person at a time, holding onto a quiet hope.",
        "Sometimes, help comes not from plans... but from people.",
    ],
    7: [
        "Kindness spreads faster than we think.",
        "With a few conversations, the missing piece finally appeared.",
        "Sometimes, it takes a community to bring a story to its ending.",
    ],
    8: [
        "For now, she chose to give it a safe place.",
        "The small room felt warmer with the cat inside.",
        "It was not a permanent answer... but it was enough for today.",
    ],
    9: [
        "Days passed, and the cat never left her side.",
        "Some bonds are not planned - they simply grow.",
        "Maybe... this was where it was meant to be all along.",
    ],
}


def image_path(filename: str) -> Path:
    return Path(__file__).parent / "images_25_6x16" / filename


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
            footer, [data-testid="stStatusWidget"] {
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
            .st-emotion-cache-tn0cau {
                gap: 0rem !important;
            }
            .main .block-container {
                max-width: 100%;
                padding-top: 0 !important;
                padding-left: 0 !important;
                padding-right: 0 !important;
            }
            .scene-image-wrap {
                position: relative;
                width: 100%;
                min-height: 100vh;
                border-radius: 0;
                overflow: hidden;
                background: #111;
            }
            .scene-image-wrap img {
                width: 100%;
                height: 100%;
                object-fit: cover;
                display: block;
            }
            .center-choice-panel {
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                width: min(500px, 85vw);
                z-index: 4;
            }
            .scene3-choice-panel {
                position: fixed;
                right: 3.5%;
                top: 28.5%;
                width: min(320px, 38vw);
                z-index: 41;
                border-radius: 16px;
                border: 1px solid rgba(255, 255, 255, 0.38);
                background: linear-gradient(
                    140deg,
                    rgba(6, 27, 44, 0.62),
                    rgba(0, 0, 0, 0.34)
                );
                backdrop-filter: blur(6px);
                padding: 12px 14px;
            }
            .choice-title {
                color: #ffffff;
                text-align: center;
                font-size: clamp(1.02rem, 2.2vw, 1.2rem);
                line-height: 1.3;
                letter-spacing: 0.01em;
                font-weight: 700;
                text-shadow: 0 2px 10px rgba(0, 0, 0, 0.45);
            }
            .end-overlay {
                position: absolute;
                left: 50%;
                bottom: 2rem;
                transform: translateX(-50%);
                z-index: 4;
                padding: 0.7rem 1.2rem;
                border-radius: 999px;
                background: rgba(0, 0, 0, 0.45);
                color: #fff;
                font-weight: 600;
            }
            .back-button {
                position: fixed;
                top: 12px;
                left: 12px;
                width: 34px;
                height: 34px;
                border-radius: 10px;
                z-index: 40;
                text-decoration: none;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 16px;
                font-weight: 700;
                color: #1f2937;
                background: linear-gradient(145deg, #d1d9e6, #ffffff);
                box-shadow: 4px 4px 8px #b8c1cc, -4px -4px 8px #ffffff;
            }
            .back-button:hover {
                box-shadow: inset 3px 3px 6px #b8c1cc, inset -3px -3px 6px #ffffff;
            }
            .back-button:active {
                transform: translateY(1px);
            }
            .narration-box {
                position: fixed;
                left: 4%;
                right: 4%;
                bottom: 16px;
                z-index: 35;
                background: rgba(0, 0, 0, 0.5);
                color: #ffffff;
                border-radius: 14px;
                padding: 16px 20px;
                min-height: 108px;
                font-size: 24px;
                line-height: 1.35;
                pointer-events: none;
                white-space: pre-wrap;
            }
            .narration-box.ready::after {
                content: "";
                position: absolute;
                right: 14px;
                bottom: 12px;
                width: 0;
                height: 0;
                border-left: 7px solid transparent;
                border-right: 7px solid transparent;
                border-top: 10px solid #ffffff;
                animation: narration-caret-bob 0.9s ease-in-out infinite;
            }
            @keyframes narration-caret-bob {
                0% {
                    transform: translateY(0);
                }
                50% {
                    transform: translateY(-5px);
                }
                100% {
                    transform: translateY(0);
                }
            }

            .typing-click-blocker {
                position: fixed;
                inset: 0;
                z-index: 60;
                background: transparent;
                pointer-events: auto;
            }

            .st-key-back_btn {
                position: fixed;
                top: 12px;
                left: 12px;
                z-index: 45;
                width: 34px;
            }
            .st-key-back_btn div[data-testid="stButton"] > button {
                width: 34px;
                height: 34px;
                min-height: 34px;
                padding: 0;
                border-radius: 10px;
                font-size: 16px;
                font-weight: 700;
                color: #1f2937;
            }

            .st-key-next_overlay {
                position: fixed;
                inset: 0;
                z-index: 30;
            }
            .st-key-next_overlay div[data-testid="stButton"] > button {
                width: 100vw;
                height: 100vh;
                min-height: 100vh;
                opacity: 0;
                border: none;
                border-radius: 0;
                box-shadow: none;
                background: transparent;
                padding: 0;
                margin: 0;
            }

            .st-key-choice_1,
            .st-key-choice_2,
            .st-key-choice_3 {
                position: fixed;
                right: 3.5%;
                width: min(320px, 38vw);
                z-index: 41;
            }
            .st-key-choice_1 {
                top: 39%;
            }
            .st-key-choice_2 {
                top: 49%;
            }
            .st-key-choice_3 {
                top: 59%;
            }
            .st-key-choice_1 div[data-testid="stButton"] > button,
            .st-key-choice_2 div[data-testid="stButton"] > button,
            .st-key-choice_3 div[data-testid="stButton"] > button {
                width: min(320px, 38vw);
                border-radius: 14px;
                border: 1px solid rgba(255, 255, 255, 0.75);
                background: rgba(255, 255, 255, 0.5);
                color: #0f172a;
                font-size: clamp(14px, 1.3vw, 16px);
                font-weight: 700;
                letter-spacing: 0.01em;
                padding: 12px 16px;
                box-shadow:
                    0 10px 18px rgba(0, 0, 0, 0.24),
                    0 3px 0 rgba(0, 0, 0, 0.22),
                    inset 0 1px 0 rgba(255, 255, 255, 0.7);
                transition: transform 0.22s ease, box-shadow 0.22s ease, filter 0.22s ease;
            }
            .st-key-choice_1 div[data-testid="stButton"] > button:hover,
            .st-key-choice_2 div[data-testid="stButton"] > button:hover,
            .st-key-choice_3 div[data-testid="stButton"] > button:hover {
                transform: translateY(-2px);
                box-shadow:
                    0 13px 24px rgba(0, 0, 0, 0.28),
                    0 4px 0 rgba(0, 0, 0, 0.2),
                    inset 0 1px 0 rgba(255, 255, 255, 0.82);
                filter: brightness(1.04);
            }
            .st-key-choice_1 div[data-testid="stButton"] > button:active,
            .st-key-choice_2 div[data-testid="stButton"] > button:active,
            .st-key-choice_3 div[data-testid="stButton"] > button:active {
                transform: translateY(4px);
                box-shadow:
                    0 4px 10px rgba(0, 0, 0, 0.26),
                    0 1px 0 rgba(0, 0, 0, 0.24),
                    inset 0 4px 10px rgba(255, 255, 255, 0.28),
                    inset 0 -2px 6px rgba(0, 0, 0, 0.1);
            }

            @media (max-width: 820px) {
                .scene3-choice-panel {
                    left: 6%;
                    right: 6%;
                    top: auto;
                    bottom: 42%;
                    width: auto;
                }
                .st-key-choice_1,
                .st-key-choice_2,
                .st-key-choice_3 {
                    left: 6%;
                    right: 6%;
                    width: auto;
                }
                .st-key-choice_1 {
                    top: auto;
                    bottom: 31%;
                }
                .st-key-choice_2 {
                    top: auto;
                    bottom: 22%;
                }
                .st-key-choice_3 {
                    top: auto;
                    bottom: 13%;
                }
                .st-key-choice_1 div[data-testid="stButton"] > button,
                .st-key-choice_2 div[data-testid="stButton"] > button,
                .st-key-choice_3 div[data-testid="stButton"] > button {
                    width: 100%;
                }
            }

            div.stButton > button {
                background: linear-gradient(145deg, #d1d9e6, #ffffff);
                border-radius: 12px;
                box-shadow: 6px 6px 12px #b8c1cc, -6px -6px 12px #ffffff;
                border: none;
                padding: 12px 24px;
                font-size: 16px;
                transition: all 0.2s ease-in-out;
                width: 100%;
            }
            div.stButton > button:hover {
                box-shadow: inset 4px 4px 8px #b8c1cc, inset -4px -4px 8px #ffffff;
            }
            div.stButton > button:active {
                transform: translateY(2px);
                box-shadow: inset 6px 6px 10px #b8c1cc, inset -6px -6px 10px #ffffff;
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


def set_scene(scene_id: int) -> None:
    st.session_state.scene = scene_id
    st.session_state.narration_index = 0
    for key in list(st.session_state.keys()):
        if key.startswith(f"typed_{scene_id}_"):
            del st.session_state[key]


def get_narration_index(scene_id: int) -> int:
    lines = NARRATIONS.get(scene_id, [])
    max_index = max(len(lines) - 1, 0)
    return max(0, min(st.session_state.get("narration_index", 0), max_index))


def render_scene_image(scene_id: int, show_end_overlay: bool = False) -> bool:
    local_image = image_path(SCENE_IMAGES[scene_id])
    if not local_image.exists():
        st.warning(f"Image not found: {SCENE_IMAGES[scene_id]}")
        return False

    image_uri = image_to_data_uri(local_image)
    end_overlay_html = '<div class="end-overlay">The End</div>' if show_end_overlay else ""
    st.markdown(
        f"""
        <div class="scene-image-wrap">
            <img src="{image_uri}" alt="Scene {scene_id}" />
            {end_overlay_html}
        </div>
        """,
        unsafe_allow_html=True,
    )
    return True


def render_choice_buttons() -> None:
    st.markdown(
        '<div class="scene3-choice-panel"><div class="choice-title">Choose your result</div></div>',
        unsafe_allow_html=True,
    )
    if st.button("Posters", key="choice_1"):
        set_scene(4)
        st.rerun()
    if st.button("Asking People", key="choice_2"):
        set_scene(5)
        st.rerun()
    if st.button("Bringing Home", key="choice_3"):
        set_scene(6)
        st.rerun()


def render_back_button(scene_id: int) -> None:
    prev_scene_id = PREV_SCENE.get(scene_id)
    if prev_scene_id is None:
        return

    if st.button("◀", key="back_btn"):
        set_scene(prev_scene_id)
        st.rerun()


def go_next(scene_id: int) -> None:
    lines = NARRATIONS.get(scene_id, [])
    idx = get_narration_index(scene_id)

    if idx < len(lines) - 1:
        st.session_state.narration_index = idx + 1
        st.rerun()

    next_scene = NEXT_SCENE.get(scene_id)
    if next_scene is not None:
        set_scene(next_scene)
        st.rerun()


def render_continue_overlay(scene_id: int) -> None:
    if st.button(" ", key="next_overlay"):
        go_next(scene_id)
        st.rerun()


def render_narration(scene_id: int, char_delay: float = 0.02) -> None:
    lines = NARRATIONS.get(scene_id, [])
    if not lines:
        return

    line_index = get_narration_index(scene_id)
    line_text = lines[line_index]
    placeholder = st.empty()
    typed_key = f"typed_{scene_id}_{line_index}"

    if st.session_state.get(typed_key, False):
        placeholder.markdown(
            f'<div class="narration-box ready">{html.escape(line_text)}</div>',
            unsafe_allow_html=True,
        )
        return

    click_blocker = st.empty()
    click_blocker.markdown('<div class="typing-click-blocker"></div>', unsafe_allow_html=True)

    current = ""
    for char in line_text:
        current += char
        placeholder.markdown(
            f'<div class="narration-box">{html.escape(current)}</div>',
            unsafe_allow_html=True,
        )
        time.sleep(char_delay)

    placeholder.markdown(
        f'<div class="narration-box ready">{html.escape(line_text)}</div>',
        unsafe_allow_html=True,
    )
    click_blocker.empty()
    st.session_state[typed_key] = True

inject_page_style()

if "scene" not in st.session_state:
    st.session_state.scene = 1
if "narration_index" not in st.session_state:
    st.session_state.narration_index = 0

current_scene = st.session_state.scene

render_back_button(current_scene)

if current_scene not in SCENE_IMAGES:
    set_scene(1)
    st.rerun()

line_index = get_narration_index(current_scene)
last_index = len(NARRATIONS.get(current_scene, [])) - 1
is_last_line = line_index >= last_index

if current_scene in NEXT_SCENE:
    rendered = render_scene_image(current_scene)
    if rendered:
        render_narration(current_scene)
        render_continue_overlay(current_scene)
elif current_scene == 3:
    rendered = render_scene_image(3)
    if rendered:
        render_narration(3)
        if is_last_line:
            render_choice_buttons()
        else:
            render_continue_overlay(3)
elif current_scene in ENDING_SCENES:
    rendered = render_scene_image(current_scene, show_end_overlay=is_last_line)
    if rendered:
        render_narration(current_scene)
        if is_last_line:
            if st.button("Restart story", key=f"restart_{current_scene}"):
                set_scene(1)
                st.rerun()
        else:
            render_continue_overlay(current_scene)
else:
    st.warning("Invalid scene configuration.")
