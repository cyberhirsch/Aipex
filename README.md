# Aipex

The top 3 AI models in every category, averaged across public leaderboards (Arena, Artificial Analysis, Hugging Face and others). Filter for open weights, and for models that run locally in 8, 24 or 32 GB of VRAM.

Live: https://cyberhirsch.github.io/Aipex/

## Update the data

1. Refresh the raw leaderboard dumps in `data/raw/` (`arena.json`, `others.json`, optional `extra-*.json`).
2. Map any new source category in `data/categories.json` (`build.py` lists unmapped ones).
3. Add open/licence/VRAM facts for new models in `data/models.json`, and name variants in `data/aliases.json`.
4. Run `python scripts/build.py` to write `data/aipex.json`.

## Tools & apps

The hand-curated tools list of the original 2024-25 site (Firebase) lives in `data/catalog.json`, converted from the raw export in `data/firebase/` by `python scripts/import_firebase.py`. Edit `data/catalog.json` directly to add or change tools.

## Score

Within one source category, a score becomes 100 × 2^(−(leader − score) / (leader − 15th place)): the leader is 100, the 15th place 50 (lower-is-better metrics measured the other way). A model's score is the mean over all sources that rank it; in categories with several sources it is pulled down toward 50 by half a board's weight, so a leader on every board beats a leader on one.

Static site: `index.html`, `style.css`, `app.js`, `data/aipex.json`, `data/catalog.json`. No build step for the page itself.
