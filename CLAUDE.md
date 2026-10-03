# UniNotes – guide for Claude

Obsidian vault with Andreas' university notes (Aalborg University, computer science → MSc machine learning).

## Layout
- `Home.md` – start page; each course folder has an `<Course> Index.md`.
- `5-semester/` … `9-semester/` – **course notes** (lectures, exercises, PDFs). Keep these separate from the ML knowledge base.
- `Machine Learning/` – **self-study ML knowledge base** (English). Entry points: `00 - Machine Learning Index.md`, `00 - Learning Path.md`, `10-Glossary/ML Formula Sheet.md`.
- `9-semester/IT-lov/` – IT law course, notes in **Danish** (`00 - IT-ret Oversigt.md`, `Noter/`). Lectures 6–7 (immaterialret + IT-kontrakter) not written yet.
- `Machine Learning/20-Play/` – interactive `ML Playgrounds.html` (vanilla JS, no dependencies), `Break the Model - Challenges.ipynb`, `Guess the Output - Quiz.ipynb` + guide notes.
- `Machine Learning/00 - Progress Dashboard.md` – Dataview dashboard. Tracked topic notes carry properties `status` (not-started|reading|done), `notebook` (not-started|in-progress|done, only if a sibling notebook exists), `level` (E|D|I|C), `reviewed` (date). Give new topic notes these properties too.
- `Journal/TIL/YYYY-MM-DD.md` – "Today I learned" daily notes (core Daily notes plugin, template `Templates/TIL.md`, inline fields `til::` and `topic::`).
- `Attachments/` – images; `Attachments/ML Animations/` – GIFs embedded in ML notes.
- `Generalt/` – misc notes, scripts, archive.

## Conventions for ML notes
- Frontmatter `tags: [ml, <topic>]`; sections: summary callout ("In one sentence") → Intuition first → The math, step by step → Worked example → Common confusions → Check yourself (`> [!question]-` callouts) → Practice (link to notebook) → Learn more (verified links only).
- Each topic note may have a sibling `<Note> - Exercises.ipynb` (saved without outputs).
- Use `[[wikilinks]]` by note name; add new notes to the index and learning path.
- Notes without notebooks/animations yet: Image Segmentation, Classical Forecasting Models, Deep Learning for Time Series, Time Series Validation and Features, Model Deployment and Serving, Experiment Tracking and Reproducibility, Data and Feature Management.

## Working rules
- Only add external links that have been verified; arXiv abs links are preferred for papers.
- Check that all wikilinks resolve before committing.
- Keep tasks small and focused (one topic or one course per session) to save usage.
