# Don's Dropper

A small pygame arcade game where **Don** drops items and **Bob** catches them.

## Gameplay

- Start on the loading screen with the message:
  - "Don is losing all his stuff. Bob must catch it all to save the world!"
- Press **Start Game** (or Enter/Space).
- Bob catches one of four falling items:
  - 🍉 watermelon
  - 🍺 beer mug
  - 🍆 eggplant
  - yellow pants
- Bob switches to a **closed-mouth** image briefly whenever an item is caught.
- The game ends after **5 misses**.
- On game over, use **Start New Game** (or Enter/Space).

## Run

```bash
python -m pip install -r requirements.txt
python dons_dropper.py
```

## Controls

- Move: Left/Right arrows or A/D
- Start/Restart from menus: Click button, Enter, or Space
- Quit: ESC or close window

## Assets / GitHub binary-file workaround

To avoid GitHub PR issues with binary image diffs, this repo does **not** require committed PNG assets.

- Don/Bob images are loaded from `assets/` **if present**.
- If those files are missing, the game renders clean fallback sprites in memory.
- Emoji drops (🍉, 🍺, 🍆) are rendered directly at runtime (no emoji PNGs required).
- Yellow pants uses `assets/pants.jpg` (or `assets/yellow_pants.png`) when available, with a fallback sprite if missing.
- Main character assets are loaded from `assets/dropper.jpg`, `assets/head_open.jpg`, and `assets/head_closed.jpg`.
- Item spawning uses a shuffled 4-item wave so each set has equal frequency: 🍉, 🍺, 🍆, and pants.
