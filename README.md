# PyCraft 0.3 — a voxel sandbox for modest laptops

Written in Python (Ursina / Panda3D + numpy). Built to run smoothly on an i3 / 8 GB laptop.
Everything in the game — blocks, mobs, sounds, music, shaders — is original.

## Run it

| Windows | `run_windows.bat` (installs the 3 libraries, then starts) |
|---|---|
| Safe mode (if anything looks wrong) | `run_safe_mode_windows.bat`  or  `python main.py --safe` |
| Linux / macOS | `./run.sh` |

Needs Python 3.10+. First start synthesises the sounds (about a second) and shows a real loading screen.

## What was wrong with the first version (and the fix)

Your gameplay video showed you were *inside* the blocks: tops invisible, black ground, hollow terrain. The
cause was inverted triangle winding in the chunk mesher, so every face was drawn inside-out. That is fixed
and verified by rendering test cubes and checking every face of the mesher against its expected direction.
The lag/freeze came from building meshes with Python loops on the main thread; the new engine meshes with
numpy on a worker thread, uploads under a small per-frame time budget, unloads far chunks, and never
touches disk on the main thread except for tiny atomic saves.

Measured (software renderer, so GPU cost excluded): game logic median 0.2–0.8 ms per frame, worst 8–15 ms
while streaming new chunks; 1,200 blocks of fast travel with memory flat at ~285 MB (view distance 5–6).

## Controls

| Key | Action |
|---|---|
| W A S D | move (arrow keys work too) |
| Mouse | look |
| Space | jump / swim up / fly up |
| Shift | sneak (never falls off edges) / fly down |
| Ctrl | sprint |
| Double-tap Space or **F** | toggle flying (creative) |
| Left click | break block / attack (hold to mine in survival) |
| Right click | place block / eat meat |
| Middle click | pick the block you look at (creative) |
| 1–9 / mouse wheel | hotbar |
| **E** | inventory (block picker) |
| **T** or **/** | chat / commands |
| **B** | soundboard |
| **F3** | debug info · **F2** screenshot · **F11** fullscreen · **Esc** pause |

## Features

* **Worlds**: infinite seeded terrain — oceans, beaches, deserts, snow, mountains, caves, clustered ores, trees, bedrock.
  Create / load / delete worlds, custom seeds, creative and survival modes, autosave every 90 s.
* **Menus**: launcher-style loading screen, title screen over a live 3D world, world list, multiplayer, options,
  soundboard, mod manager, pause, inventory, death screen.
* **Looks**: ambient occlusion, day/night cycle with sunsets, sun, moon, stars, clouds, fog, translucent water,
  block-break particles, held block, hearts, selection outline, mining cracks.
* **Shader packs** (Options → Shader pack): `off` (fixed-function, fastest), `lite`, `vivid`, `cinematic`.
  If a shader fails to compile on your GPU the game falls back to `off` by itself.
* **Resource packs** (Options → Resource pack): see `resourcepacks/README.txt`. Included: `procedural` (original art)
  and `patrix` (your copy of the Patrix tiles; baked tint for grass/leaves). Switch live, no restart.
* **Mobs**: boar, woolly, hen (friendly, flee when hit, drop meat in survival) and the shambler (hostile at night
  and in caves, weakened by daylight). Fixed 20 Hz AI with render interpolation, only near the player.
* **Sound**: 160+ synthesised sounds — per-material break/place/step/hit, splashes, mob voices, hurt/death, UI —
  plus three generated music tracks. No audio device? The game just stays silent.
* **Soundboard**: 15 built-in clips + any `.wav/.ogg/.mp3` you drop into `sounds/soundboard/`. In multiplayer
  everyone hears it.
* **Mods**: drop `.py` files into `mods/` (see `mods/README.txt`; 3 examples included: lamps & gems, jetpack, fun commands).
* **LAN multiplayer**: pause → *Open to LAN*, or *Multiplayer → Host*. Friends on the same Wi-Fi see your game
  automatically or type your IP. Block edits, players with name tags, mobs, chat and soundboard are synced.
* **Survival**: health & hearts, regeneration, fall damage, mining time by block hardness, collected blocks, respawn.
* **Safety nets**: crash guard (an error in one frame is logged to `crash.log` and the game keeps running),
  auto-performance guard (lowers view distance if FPS stays low), broken mods switch themselves off.

## Commands (press T or /)

`/help` `/gamemode creative|survival` `/tp x y z` (or `/tp <player>`) `/time day|noon|sunset|night|midnight`
`/give <block> [n]` `/summon boar|woolly|hen|shambler [n]` `/kill` `/fly` `/speed n` `/sound <name>` `/shader <name>`
`/rd <2-16>` `/mods` `/blocks` `/list` `/pos` `/seed` `/spawn` `/heal` `/save` `/say` `/debug` — plus mod commands.

## If it is slow

1. Options → Shader = `off`, View distance = 3.
2. Leave "Auto performance guard" on.
3. Close other heavy programs; keep the laptop plugged in.

## Tests

`python tests/test_world.py` (streaming, edits, saves, physics) and `python tests/test_net.py` (LAN protocol).

## Credits / legal

Original code and assets. Patrix textures are used only from the copy you supplied, for personal use
(credit: Patrix). Not affiliated with Mojang or Microsoft; no Mojang files are included.
