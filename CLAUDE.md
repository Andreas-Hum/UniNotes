# UniNotes – guide for Claude

Obsidian vault with Andreas' university notes (Aalborg University, computer science → MSc machine learning).

## Layout
- `Home.md` – start page; each course folder has an `<Course> Index.md`.
- `5-semester/` … `9-semester/` – **course notes** (lectures, exercises, PDFs). Keep these separate from the ML knowledge base.
- `Machine Learning/` – **self-study ML knowledge base** (English). Entry points: `00 - Machine Learning Index.md`, `00 - Learning Path.md`, `10-Glossary/ML Formula Sheet.md`.
- `9-semester/IT-lov/` – IT law course, notes in **Danish** (`00 - IT-ret Oversigt.md`, `Noter/`). Lectures 6–7 (immaterialret + IT-kontrakter) not written yet.
- `Machine Learning/20-Play/` – interactive `ML Playgrounds.html` (vanilla JS, no dependencies), `Break the Model - Challenges.ipynb`, `Guess the Output - Quiz.ipynb` + guide notes.
- `Machine Learning/21-Learn-from-the-Masters/` – `Paper-to-Code Months.md` + `Paper-to-Code 1–4` notebooks (ResNet, word2vec, LightGCN, DDPM; need PyTorch, download data to `./data`, gitignored) and `Explain-it Videos.md` + Manim example `explain_it_gradient_descent.py` (Text only, no LaTeX; preview MP4 in `Attachments/ML Animations/`).
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
2. **Weekly mini-challenge** – one small dataset per week, sized for one evening, Kaggle-style.
   - A note `Weekly Challenges.md` listing challenges + one notebook per challenge (`Weekly Challenge NN - <name>.ipynb`): story, data loading (prefer offline sklearn/bundled datasets or small public CSVs with verified URLs), a baseline score, a **target score to beat**, an evaluation cell that prints ✅/❌ against the target, and a hidden solution walkthrough (collapsed `<details>` markdown) explaining the winning approach.
   - Start with ~4 challenges of mixed type (tabular classification, regression, text, time series), increasing difficulty.
3. **Beat-the-baseline leaderboard** – a note `Leaderboard.md` where Andreas logs his best scores on fixed tasks and tries to improve over time.
   - Fixed tasks with fixed splits/metrics so scores are comparable: MNIST (test accuracy), MovieLens 100K (NDCG@10, reuse the split from the MovieLens project notebooks in `12-Recommender-Systems/`), and one forecasting set (MASE on a fixed holdout).
   - Each task: a short spec (data, split, metric, rules), a provided baseline score, and a Markdown table (date · score · method · notebook link) to append to. A helper snippet that computes the metric the official way. Optionally add a Dataview block to `00 - Progress Dashboard.md` showing the current best per task.
