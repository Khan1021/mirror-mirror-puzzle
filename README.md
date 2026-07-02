# mirror-mirror-puzzle

A puzzle game distilled into a function that takes two inputs — a world configuration and a
movement instructions string ("WASDX") — and returns the final game state plus every
intermediate step along the way.

The core game logic is written in Python (`core.py`); the visualization is written in
TypeScript (`src/main.ts`), rendering the steps as an emoji grid in the browser.

See `Assumptions.md` for the interpretation decisions made where the brief was ambiguous
(most notably, how the `X` mirror-teleport mechanic works).

## Project layout

- `core.py` — game state, movement, mirror reflection, and the `X` teleport mechanic
- `test_core.py` — unit tests for `core.py`
- `export.py` — builds a sample world, runs it, and writes `game_data.json`
- `game_data.json` — output of `export.py`, consumed by the browser visualization
- `src/main.ts` / `dist/main.js` — TypeScript visualization (source and compiled output)
- `index.html` — loads the visualization in a browser

## Running the Python core + tests

Requires Python 3. No third-party dependencies.

```
python export.py          # regenerates game_data.json from the sample world
python -m unittest test_core -v   # runs the test suite
```

## Running the visualization

Requires Node.js (for the TypeScript compiler).

```
npm install                # installs TypeScript (only needed once)
npx tsc                    # compiles src/main.ts -> dist/main.js
python export.py           # generates game_data.json (skip if already generated)
python -m http.server 8000 # serves the project so the browser can fetch game_data.json
```

Then open `http://localhost:8000/index.html` in a browser. Use the Prev/Next buttons to step
through every move in the instruction sequence.

Note: `index.html` must be loaded via `http://localhost:...`, not by double-clicking the file
directly — browsers block ES module scripts and `fetch` requests from the `file://` protocol.
