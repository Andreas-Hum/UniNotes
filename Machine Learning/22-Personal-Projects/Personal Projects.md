---
tags: [ml, project, play]
status: not-started
level: I
reviewed:
---
# Personal Projects

> [!summary] In one sentence
> Five end-to-end projects on data **you** care about: your own Danish notes, your movie taste and Spotify history, Danish electricity prices, your vault as a chatbot, and Danish mushrooms. Each has a guide note and a notebook with TODOs, ✅ checks and hidden solutions.

Exercises use clean datasets someone else picked. These projects use *your* data, which is where the real problems are: messy exports, tiny datasets, time zones, licences, "is this result good?". Each runs on a laptop CPU in a few minutes.

| Project | You build | Key result with the reference solution | Notebook |
|---|---|---|---|
| [[Mini-GPT on Danish]] | a character-level GPT from scratch, trained on your IT-ret notes | val loss **1.66** vs bigram **2.65**; writes nonsense Danish legalese | [open](Mini-GPT%20on%20Danish%20-%20Notebook.ipynb) |
| [[My Own Recommender]] | ALS + fold-in for *you* on MovieLens, a content hybrid, artist embeddings from Spotify | ALS RMSE **0.849** vs biases **0.861**; demo clusters recovered | [open](My%20Own%20Recommender%20-%20Notebook.ipynb) |
| [[Danish Electricity Prices]] | a day-ahead price forecaster for DK1 with Energi Data Service + DMI data | MAE **29.6 → 21.8** EUR/MWh once wind & solar forecasts are added | [open](Danish%20Electricity%20Prices%20-%20Notebook.ipynb) |
| [[RAG over My Notes]] | chunking, TF-IDF + multilingual embeddings, hybrid search, eval set, Claude answers with note links | hit@3: TF-IDF **0.80**, embeddings **0.95**, hybrid **0.95** | [open](RAG%20over%20My%20Notes%20-%20Notebook.ipynb) |
| [[Danish Mushroom Classifier]] | transfer learning on 360 iNaturalist photos from Denmark (or your own photos) | ResNet-18 linear probe **87 %** vs from-scratch CNN **38 %** | [open](Danish%20Mushroom%20Classifier%20-%20Notebook.ipynb) |

**Suggested order:** Electricity (classic ML, quick win) → Recommender → Mushrooms → Mini-GPT → RAG. That order follows the [[00 - Learning Path]] from tabular models to deep learning to LLMs. They're independent, so start with whichever sounds most fun.

**Setup:** `pip install torch torchvision scikit-learn pandas matplotlib`, plus `sentence-transformers` (and optionally `anthropic`) for the RAG project. Every notebook downloads its data into `22-Personal-Projects/data/` (git-ignored). Downloaded data and your personal exports never get committed.

**Grows with you:** the mini-GPT and the RAG chatbot read your vault every time they run, so each new IT-ret lecture you write makes the GPT's Danish better and the chatbot's answers broader.

## Ideas for after
- Combine them: use the RAG chatbot to quiz yourself before the IT-ret exam; feed the mini-GPT your song lyrics; forecast your own electricity bill with the price model.
- Log your best scores on the [[Leaderboard]] tasks with the same habits: fixed split, baseline first, one change at a time.
- Turn one into an [[Explain-it Videos|Explain-it video]]: "Why wind makes Danish power cheap" is a great 3-minute story.

---
Back to [[00 - Machine Learning Index]].
