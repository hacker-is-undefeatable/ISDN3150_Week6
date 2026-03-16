# Streamlit Story Website

## Run locally

1. Create and activate your Python environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the app:
   ```bash
   streamlit run app.py
   ```

## Project structure

- `app.py`: main interactive website
- `assets/images/`: place generated chapter images here (`chapter1.png` ... `chapter4.png`)
- `assets/audio/`: optional narration audio (`narration.mp3`)

## What to customize

- Update `STORY_CHAPTERS` in `app.py` with your own story.
- Add your generated images into `assets/images/`.
- Keep the `Workflow Note` tab content aligned with your real design process.
