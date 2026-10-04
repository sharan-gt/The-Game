# Developer notes / how to resume

Status (checkpoint 1): game boots, title screen over live world, create/load worlds, play creative & survival,
mobs, sounds, soundboard, mods, shaders, resource packs, LAN multiplayer code. Tests: tests/test_world.py,
tests/test_net.py pass. Headless smoke/soak/trek tests passed (see README "Measured").

Architecture
* `engine/` pure logic: blocks, procgen (original textures), atlas (padded POT atlas + icons), meshing (numpy,
  per-vertex AO, winding (0,2,1)/(0,3,2) — DO NOT change, it is the "broken blocks" fix), terrain, world
  (chunk streaming + worker thread + saves), physics, raycast, render (Panda geometry from numpy, GLSL
  presets, sky helpers), audio (numpy synth), mobs, mods, commands.
* `game/` Ursina layer: app.py (Game state machine), screens.py (menus), ui.py (widgets), hud.py, player.py, fx.py.
* `net/` newline-JSON TCP server/client + UDP LAN discovery.

Known gaps / ideas (not done yet)
* Two-process host/join integration test of the full game (protocol tested alone).
* More resource packs (generator script for extra procedural packs), more shader presets.
* Water does not flow; no crafting/tools/furnaces; mobs only target the host player.
* Window-resize handling for shader `screen` uniform (cinematic vignette is a HUD overlay instead).

Test recipe (headless): `xvfb-run -a --server-args="-screen 0 1100x640x24" python3 smoke.py`
(see tests/ — create Ursina(development_mode=False,...), loop `app.taskMgr.step(); game.tick(dt)`).
Gotchas learned: start Xvfb + python in ONE shell call; Ursina color.rgb is 0-1; never keep a removed
NodePath in renderer groups (renderer prunes empty paths now).
