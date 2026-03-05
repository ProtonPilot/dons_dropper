# Don's Dropper

A small pygame arcade game where **Don** drops items and **Bob** catches them.

## Gameplay

- Start on the loading screen with the message:
  - "Don is losing all his stuff. Bob must catch it all to save the world!"
- Press **Start Game** (or Enter/Space).
- Bob catches one of four falling items:
  - watermelon emoji-styled icon
  - beer mug emoji-styled icon
  - eggplant emoji-styled icon
  - yellow pants (from `assets/yellow_pants.png`)
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

To avoid GitHub PR binary-file issues, PNG files are not committed by this branch.

You should keep your provided local images in `assets/`:

- `assets/don.png`
- `assets/bob_open.png`
- `assets/bob_closed.png`
- `assets/yellow_pants.png`

The game now **requires** those local files for Don/Bob/pants, and generates the other three emoji-style drop icons directly in memory at runtime.
