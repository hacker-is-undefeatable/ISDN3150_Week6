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

ENDING_SCENES = {7, 8, 9}

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
        "She decided to leave a message behind, in case someone was searching.",
        "Each poster she placed carried a quiet hope — that it would reach the right person.",
        "She stepped back and looked at it, wondering if it would be enough.",
    ],
    5: [
        "She gathered her courage and began asking around, hoping someone might recognize the little cat.",
        "Most people shook their heads, but each question felt like a step closer to an answer.",
        "Just as doubt began to settle in, someone paused… and looked a little more closely.",
    ],
    6: [
        "She couldn’t leave it behind, not like this.",
        "Carefully, she brought the cat home, offering it a quiet place to rest.",
        "For the first time, it relaxed — as if it finally felt safe.",
    ],
    7: [
        "A call came sooner than she expected.",
        "When the owner arrived, the cat ran forward without hesitation.",
        "Watching them reunite, she felt a quiet warmth, some goodbyes are also happy endings.",
    ],
    8: [
        "One small conversation led to another, until the right person finally appeared.",
        "The pieces came together, not by chance, but through the kindness of strangers.",
        "In the end, it wasn’t just her who helped the cat — it was everyone.",
    ],
    9: [
        "Days turned into something softer, something familiar.",
        "The cat stayed, never straying far from her side.",
        "Without realizing it, they had already become a part of each other’s lives.",
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
            .scene-transition-wrap {
                position: fixed;
                inset: 0;
                z-index: 90;
                overflow: hidden;
                background: #000;
                pointer-events: none;
                animation: scene-overlay-dismiss 0.01s linear 0.68s forwards;
            }
            .scene-transition-wrap img {
                position: absolute;
                inset: 0;
                width: 100%;
                height: 100%;
                object-fit: cover;
            }
            .scene-transition-from {
                animation: scene-fade-out 0.65s ease-in-out forwards;
            }
            .scene-transition-to {
                opacity: 0;
                animation: scene-fade-in 0.65s ease-in-out forwards;
            }
            @keyframes scene-fade-out {
                from {
                    opacity: 1;
                }
                to {
                    opacity: 0;
                }
            }
            @keyframes scene-fade-in {
                from {
                    opacity: 0;
                }
                to {
                    opacity: 1;
                }
            }
            @keyframes scene-overlay-dismiss {
                to {
                    opacity: 0;
                    visibility: hidden;
                }
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
            .st-key-choice_3,
            .st-key-ending_try_other,
            .st-key-ending_rewatch {
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
            .st-key-ending_try_other {
                top: 49%;
            }
            .st-key-ending_rewatch {
                top: 59%;
            }
            .st-key-choice_1 div[data-testid="stButton"] > button,
            .st-key-choice_2 div[data-testid="stButton"] > button,
            .st-key-choice_3 div[data-testid="stButton"] > button,
            .st-key-ending_try_other div[data-testid="stButton"] > button,
            .st-key-ending_rewatch div[data-testid="stButton"] > button {
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
            .st-key-choice_3 div[data-testid="stButton"] > button:hover,
            .st-key-ending_try_other div[data-testid="stButton"] > button:hover,
            .st-key-ending_rewatch div[data-testid="stButton"] > button:hover {
                transform: translateY(-2px);
                box-shadow:
                    0 13px 24px rgba(0, 0, 0, 0.28),
                    0 4px 0 rgba(0, 0, 0, 0.2),
                    inset 0 1px 0 rgba(255, 255, 255, 0.82);
                filter: brightness(1.04);
            }
            .st-key-choice_1 div[data-testid="stButton"] > button:active,
            .st-key-choice_2 div[data-testid="stButton"] > button:active,
            .st-key-choice_3 div[data-testid="stButton"] > button:active,
            .st-key-ending_try_other div[data-testid="stButton"] > button:active,
            .st-key-ending_rewatch div[data-testid="stButton"] > button:active {
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
                .st-key-choice_3,
                .st-key-ending_try_other,
                .st-key-ending_rewatch {
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
                .st-key-ending_try_other {
                    top: auto;
                    bottom: 22%;
                }
                .st-key-ending_rewatch {
                    top: auto;
                    bottom: 13%;
                }
                .st-key-choice_1 div[data-testid="stButton"] > button,
                .st-key-choice_2 div[data-testid="stButton"] > button,
                .st-key-choice_3 div[data-testid="stButton"] > button,
                .st-key-ending_try_other div[data-testid="stButton"] > button,
                .st-key-ending_rewatch div[data-testid="stButton"] > button {
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
    st.session_state.scene3_choices_hidden = scene_id != 3
    for key in list(st.session_state.keys()):
        if key.startswith(f"typed_{scene_id}_"):
            del st.session_state[key]


def start_scene_transition(target_scene_id: int) -> None:
    current_scene = st.session_state.get("scene", 1)
    if current_scene == 3:
        st.session_state.scene3_choices_hidden = True
    st.session_state.transition_from_scene = current_scene
    st.session_state.transition_to_scene = target_scene_id
    st.session_state.transition_active = True
    # Switch the logical scene immediately so reruns never flash the previous scene.
    set_scene(target_scene_id)


def render_scene_transition() -> None:
    if not st.session_state.get("transition_active", False):
        return

    from_scene = st.session_state.get("transition_from_scene")
    to_scene = st.session_state.get("transition_to_scene")
    if from_scene not in SCENE_IMAGES or to_scene not in SCENE_IMAGES:
        st.session_state.transition_active = False
        st.session_state.transition_from_scene = None
        st.session_state.transition_to_scene = None
        return

    from_image = image_path(SCENE_IMAGES[from_scene])
    to_image = image_path(SCENE_IMAGES[to_scene])
    if not from_image.exists() or not to_image.exists():
        st.session_state.transition_active = False
        st.session_state.transition_from_scene = None
        st.session_state.transition_to_scene = None
        return

    from_uri = image_to_data_uri(from_image)
    to_uri = image_to_data_uri(to_image)
    st.markdown(
        f"""
        <div class="scene-transition-wrap">
            <img src="{from_uri}" alt="Scene {from_scene}" class="scene-transition-from" />
            <img src="{to_uri}" alt="Scene {to_scene}" class="scene-transition-to" />
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Keep transition overlay for this render only; avoid an extra rerun that can flash old UI.
    st.session_state.transition_active = False
    st.session_state.transition_from_scene = None
    st.session_state.transition_to_scene = None
    return


def hide_scene3_choice_ui_when_not_needed(scene_id: int) -> None:
    if scene_id == 3:
        return

    st.markdown(
        """
        <style>
            .scene3-choice-panel,
            .st-key-choice_1,
            .st-key-choice_2,
            .st-key-choice_3 {
                display: none !important;
                opacity: 0 !important;
                visibility: hidden !important;
                pointer-events: none !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def hide_ending_buttons_when_not_needed(scene_id: int, is_last_line: bool) -> None:
    if scene_id in ENDING_SCENES and is_last_line:
        return

    st.markdown(
        """
        <style>
            .st-key-ending_try_other,
            .st-key-ending_rewatch {
                display: none !important;
                opacity: 0 !important;
                visibility: hidden !important;
                pointer-events: none !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


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
    if st.session_state.get("scene3_choices_hidden", False):
        return

    st.markdown(
        '<div class="scene3-choice-panel"><div class="choice-title">Choose your result</div></div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <script>
            if (!window.scene3InstantHideBound) {
                window.scene3InstantHideBound = true;
                document.addEventListener("pointerdown", function (event) {
                    const choiceButton = event.target.closest(
                        ".st-key-choice_1 button, .st-key-choice_2 button, .st-key-choice_3 button"
                    );
                    if (!choiceButton) {
                        return;
                    }

                    const targets = document.querySelectorAll(
                        ".scene3-choice-panel, .st-key-choice_1, .st-key-choice_2, .st-key-choice_3"
                    );
                    targets.forEach((node) => {
                        node.style.display = "none";
                        node.style.pointerEvents = "none";
                    });
                });
            }
        </script>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Posters", key="choice_1"):
        st.session_state.scene3_choices_hidden = True
        start_scene_transition(4)
        st.rerun()
    if st.button("Asking People", key="choice_2"):
        st.session_state.scene3_choices_hidden = True
        start_scene_transition(5)
        st.rerun()
    if st.button("Bringing Home", key="choice_3"):
        st.session_state.scene3_choices_hidden = True
        start_scene_transition(6)
        st.rerun()


def render_ending_buttons() -> None:
    if st.button("Try another ending", key="ending_try_other"):
        start_scene_transition(3)
        st.rerun()

    if st.button("Re-watch", key="ending_rewatch"):
        start_scene_transition(1)
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
if "transition_active" not in st.session_state:
    st.session_state.transition_active = False
if "transition_from_scene" not in st.session_state:
    st.session_state.transition_from_scene = None
if "transition_to_scene" not in st.session_state:
    st.session_state.transition_to_scene = None
if "scene3_choices_hidden" not in st.session_state:
    st.session_state.scene3_choices_hidden = st.session_state.scene != 3

render_scene_transition()

current_scene = st.session_state.scene

render_back_button(current_scene)

if current_scene not in SCENE_IMAGES:
    set_scene(1)
    st.rerun()

line_index = get_narration_index(current_scene)
last_index = len(NARRATIONS.get(current_scene, [])) - 1
is_last_line = line_index >= last_index

hide_scene3_choice_ui_when_not_needed(current_scene)
hide_ending_buttons_when_not_needed(current_scene, is_last_line)

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
            render_ending_buttons()
        else:
            render_continue_overlay(current_scene)
else:
    st.warning("Invalid scene configuration.")
