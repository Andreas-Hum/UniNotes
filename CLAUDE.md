# UniNotes – guide for Claude

Obsidian vault with Andreas' university notes (Aalborg University, computer science → MSc machine learning).

## Layout
- `Home.md` – start page; each course folder has an `<Course> Index.md`.
- `5-semester/` … `9-semester/` – **course notes** (lectures, exercises, PDFs). Keep these separate from the ML knowledge base.
- `Machine Learning/` – **self-study ML knowledge base** (English). Entry points: `00 - Machine Learning Index.md`, `00 - Learning Path.md`, `10-Glossary/ML Formula Sheet.md`.
- `9-semester/IT-lov/` – IT law course, notes in **Danish** (`00 - IT-ret Oversigt.md`, `Noter/`). Lectures 6–7 (immaterialret + IT-kontrakter) not written yet.
- `Machine Learning/20-Play/` – interactive `ML Playgrounds.html` (vanilla JS, no dependencies), `Break the Model - Challenges.ipynb`, `Guess the Output - Quiz.ipynb`, `Weekly Challenge NN - <name>.ipynb` (listed in `Weekly Challenges.md`; cells tagged `your-solution` / `evaluate` / `solution` so the ```python block in the solution can be substituted for testing) + guide notes.
- `Machine Learning/20-Play/Leaderboard.md` – beat-the-baseline leaderboard: 3 fixed tasks (MNIST accuracy, MovieLens `ml-latest-small` full-ranking NDCG@10 on the project split, M4 Hourly MASE) with starter notebooks `Leaderboard - <Task>.ipynb` (data cached in git-ignored `leaderboard-data/`, split fingerprints, official metric, baseline check). Results are Markdown table rows; a dataviewjs block parses them for "current best" (also on the dashboard). Don't change splits, metrics or baselines – it would break comparability.
- `Machine Learning/21-Learn-from-the-Masters/` – `Paper-to-Code Months.md` + `Paper-to-Code 1–4` notebooks (ResNet, word2vec, LightGCN, DDPM; need PyTorch, download data to `./data`, gitignored) and `Explain-it Videos.md` + Manim example `explain_it_gradient_descent.py` (Text only, no LaTeX; preview MP4 in `Attachments/ML Animations/`).
- `Machine Learning/22-Personal-Projects/` – `Personal Projects.md` + 5 project notes, each with `<Note> - Notebook.ipynb`: Mini-GPT on Danish (trains on `9-semester/IT-lov/` + `data/my_text/*.txt`), My Own Recommender (MovieLens fold-in + Spotify export in `data/spotify/`, synthetic demo fallback), Danish Electricity Prices (Energi Data Service + DMI, fixed Oct 2023–Sep 2025 window), RAG over My Notes (sentence-transformers e5, embedding cache in `data/`, optional `ANTHROPIC_API_KEY`), Danish Mushroom Classifier (iNaturalist download or `data/my_photos/`). All data under `22-Personal-Projects/data/` is git-ignored – never commit personal exports.
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

## Backlog – next "learn by doing" projects (one per session)
Put new work in `Machine Learning/20-Play/` (link it from `00 - Machine Learning Index.md` §20 Play, the learning path and `20-Play` guide notes). Keep the same quality bar as the existing Play items: test notebooks with nbclient (run as delivered without errors; with solutions filled in, every check passes), test HTML in headless Chromium, verify every claimed number.

1. **RL agent on a game** – train an agent from tabular Q-learning up to DQN and watch it improve.
   - Build a **new**, self-contained Snake game from scratch inside `Machine Learning/20-Play/`: a headless, gym-like environment (`reset()`, `step(action) → state, reward, done`) in plain NumPy so it trains fast, plus a simple way to watch a trained agent play (e.g. matplotlib animation or a small HTML/canvas replay).
   - Milestones: (1) environment + random-agent baseline, (2) tabular Q-learning on a compact state (danger ahead/left/right, food direction, heading), (3) DQN in PyTorch (replay buffer, target network, ε-schedule), (4) compare all agents on average score. Plot learning curves (score per episode). Optional extensions: Flappy Bird or Connect Four (self-play / minimax opponent).
   - Link to [[RL Basics and MDPs]] and [[Q-Learning and Policy Gradients]].
2. ✅ **Weekly mini-challenge** – done (weeks 01–04 in `20-Play/`; add new weeks the same way). Original spec: one small dataset per week, sized for one evening, Kaggle-style.
   - A note `Weekly Challenges.md` listing challenges + one notebook per challenge (`Weekly Challenge NN - <name>.ipynb`): story, data loading (prefer offline sklearn/bundled datasets or small public CSVs with verified URLs), a baseline score, a **target score to beat**, an evaluation cell that prints ✅/❌ against the target, and a hidden solution walkthrough (collapsed `<details>` markdown) explaining the winning approach.
   - Start with ~4 challenges of mixed type (tabular classification, regression, text, time series), increasing difficulty.
