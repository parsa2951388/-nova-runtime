# FRAMEZERO LAB desktop console

## Launch

With Python 3.12+ and recursive submodules initialized:

~~~sh
python framezero_gui.py
~~~

The desktop console uses Python's standard-library Tk interface. No additional Python package is required where Tk support is included in the Python installation.

## Overview

The console includes:

- Project identity and the exact pinned engine identifier.
- Upstream status snapshot, explicitly labelled as upstream-reported.
- Local environment diagnostics and detected versions.
- Local package folder selection, validation, output folder and optional work folder.
- Runtime-only, asset-export, and full upstream build profiles.
- Live child-process output.
- Stop and bounded force-stop controls.

## Build profiles

| Profile | Upstream arguments | Upstream storage estimate |
|---|---|---|
| Runtime | --stages check,shaders,runtime | About 30 GiB |
| Assets | --stages check,assets | About 370 GiB |
| Full | Default upstream stages | About 400 GiB |

These figures are upstream estimates, not guarantees.

## Process and thread safety

Tk widgets are only changed on the Tk main thread. Child processes are created before the Stop button is enabled. A worker thread reads process output and forwards it through a thread-safe queue. Stop requests normal termination and schedules a force-stop check if the process remains active.

## Limitations

- The console does not download, decrypt, or modify a package.
- It does not bundle game data, keys, or proprietary assets.
- It does not claim that a game is playable.
- It has no game-launch action.
- Build behavior and flags belong to the pinned upstream engine.
- It does not silently install prerequisites.
