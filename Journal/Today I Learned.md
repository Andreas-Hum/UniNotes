---
tags: [til, journal]
---
# Today I Learned

One line a day. That's all. After a semester you have a hundred pieces of evidence that you are learning – the best antidote to [[Imposter Syndrome]].

## How to write today's line
1. Command palette (`Ctrl/Cmd + P`) → **Daily notes: Open today's daily note** (or click the calendar icon in the left ribbon). It creates `Journal/TIL/YYYY-MM-DD.md` from the template.
2. Fill in the two lines:
```
til:: Ridge regression never sets a coefficient exactly to zero – Lasso does, because of the corner in the L1 ball.
topic:: [[Overfitting and Regularization]]
```
Several topics: `topic:: [[PCA]], [[Linear Algebra for ML]]`.

## Why it works
- **Retrieval:** writing it in your own words is a mini-recall exercise.
- **Links:** the topic link puts the entry in that note's backlinks, so when you reopen *Overfitting and Regularization* you see everything you learned about it.
- **Visibility:** the [[00 - Progress Dashboard|Progress Dashboard]] shows your streak, total count and most-learned topics.

## Ideas when you're stuck
- A formula you finally understood (check the [[ML Formula Sheet]]).
- A "Guess the Output" question you got wrong ([[Guess the Output]]).
- Something from a lecture, paper or video – not only ML: IT-ret, other courses, anything.
- A mistake you made in code and how you fixed it.

All entries live in `Journal/TIL/`.
