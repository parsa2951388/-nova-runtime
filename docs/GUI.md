# NOVA desktop setup console

## Launch

With Python 3.12+ and the repository submodules initialized:

```sh
python nova_gui.py
```

The GUI uses Python's standard-library Tk interface. No extra Python package is required where Tk support is included with Python.

## What it does

- Shows the NOVA identity and the exact pinned engine identifier.
- Runs the NOVA environment doctor and displays its results in a diagnostics table.
- Opens the upstream engine help.
- Runs the upstream package finder.
- Lets the user choose a local package folder, output folder, and optional work folder.
- Supports package validation, the reduced runtime build profile, the asset-export profile, and the full upstream default pipeline.
- Streams process output into an activity log and allows a running process to be stopped.

## Build profiles

| Profile | Upstream arguments | Upstream storage estimate |
|---|---|---|
| Runtime | `--stages check,shaders,runtime` | About 30 GiB |
| Assets | `--stages check,assets` | About 370 GiB |
| Full | No `--stages` override; upstream default | About 400 GiB |

The estimates are from the pinned upstream documentation and are not guarantees for every system.

## Explicit limitations

- The console does not download, decrypt, or modify a game package.
- It does not bundle game data, keys, or executables.
- It does not claim that the game is playable and does not offer a game-launch button.
- All build flags and actual build behavior are owned by the pinned upstream engine.
- A failed or missing prerequisite is shown as a diagnostic; the GUI does not silently install software.

The GUI is a setup and build front end, not a completed game launcher.
