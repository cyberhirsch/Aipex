# Aipex

The top 3 AI models in every category, averaged across public leaderboards (Arena, Artificial Analysis, Hugging Face and others). Filter for open weights, and for models that run locally in 8, 24 or 32 GB of VRAM.

Live: https://cyberhirsch.github.io/Aipex/

## Update the data

1. Refresh the raw leaderboard dumps in `data/raw/` (`arena.json`, `others.json`, optional `extra-*.json`).
2. Map any new source category in `data/categories.json` (`build.py` lists unmapped ones).
3. Add open/licence/VRAM facts for new models in `data/models.json`, and name variants in `data/aliases.json`.
4. Run `python scripts/build.py` to write `data/aipex.json`.

## Score

Within one source category, scores are rescaled so the leader is 100 and the 15th entry is 0 (lower-is-better metrics inverted). A model's score is the mean over all sources that rank it in that category.

Static site: `index.html`, `style.css`, `app.js`, `data/aipex.json`. No build step for the page itself.
