#!/usr/bin/env python3
"""PyCraft - a voxel sandbox for modest laptops.

    python main.py            normal start
    python main.py --safe     fixed-function renderer, short view distance (if anything misbehaves)
"""
import os
import sys
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parent
os.chdir(ROOT)
sys.path.insert(0, str(ROOT))
SAFE = "--safe" in sys.argv


def main():
    from ursina import Entity, Ursina, application, window
    from ursina import time as utime
    from engine import settings

    size = (1100, 640)
    app = Ursina(title=settings.TITLE, development_mode=False, fullscreen=False, borderless=False,
                 vsync=True, size=size, show_ursina_splash=False, editor_ui_enabled=False)
    for attr in ("exit_button", "fps_counter", "cog_button", "entity_counter", "collider_counter"):
        try:
            w = getattr(window, attr)
            w.enabled = False
            w.visible = False
        except Exception:
            pass

    from game.app import Game
    game = Game(app, safe=SAFE)

    class Director(Entity):
        def update(self):
            game.tick(utime.dt)

        def input(self, key):
            try:
                game.on_key(key)
            except Exception:
                traceback.print_exc()

    Director()
    app.run()


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except BaseException:
        tb = traceback.format_exc()
        try:
            (ROOT / "crash.log").write_text(tb)
        except OSError:
            pass
        print(tb)
        print("\nPyCraft crashed on startup. Details were saved to crash.log.\n"
              "Try:  python main.py --safe")
        input("Press Enter to close...")
