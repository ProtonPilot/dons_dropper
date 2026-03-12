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
# Optional but recommended for robust JPG decoding fallback:
python -m pip install pillow
python dons_dropper.py
# Silence startup asset debug logs if desired:
DONS_DROPPER_DEBUG_ASSETS=0 python dons_dropper.py
```

## Controls

- Move: Left/Right arrows or A/D
- Start/Restart from menus: Click button, Enter, or Space
- Quit: ESC or close window

## Assets / GitHub binary-file workaround

To avoid GitHub PR issues with binary image diffs, this repo does **not** require committed PNG assets.

- Don/Bob images are loaded from nearby `assets/` folders (script dir, cwd, and parent directories) to make startup-location issues less likely.
- JPG/PNG decoding first uses pygame and then automatically falls back to Pillow (if installed) for files pygame cannot decode.
- If those files are missing, the game renders clean fallback sprites in memory.
- Emoji drops (🍉, 🍺, 🍆) are rendered directly at runtime when emoji fonts are available; if the font only returns missing-glyph boxes, the game now falls back to built-in icon art instead of placeholder text.
- You can optionally provide `assets/watermelon.png|jpg`, `assets/beer_mug.png|jpg`, and `assets/eggplant.png|jpg` to guarantee image-based drops on systems without emoji fonts.
- Yellow pants uses `assets/pants.jpg` when available, with a fallback sprite if missing.
- Main character assets are loaded from `assets/dropper.jpg`, `assets/head_open.jpg`, and `assets/head_closed.jpg`.
- Item spawning uses a shuffled 4-item wave so each set has equal frequency: 🍉, 🍺, 🍆, and pants (from `assets/pants.jpg`).
