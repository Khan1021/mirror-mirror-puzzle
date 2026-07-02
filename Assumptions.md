# Assumptions

The brief left several mechanics open to interpretation, since it's described mostly through
examples. Decisions made, and why:

## Win condition
The character wins by ending up on the same cell as the crate — either by walking onto it
(`W`/`A`/`S`/`D`) or by teleporting onto it (`X`). In both cases the crate is removed and
`run_game` returns `(True, steps)`.

## `X` teleports the character (rather than firing a separate, non-moving projectile)
Based on the visual reference material, the "glowing projectile" represents a possible teleport
destination for the character, not a separate object. Pressing `X`:

1. **Phase 1** — simulate the projectile leaving the character in the direction it's currently
   facing, counting how many cells it travels.
   - If it reaches a `Mirror` first, note the distance travelled and continue to Phase 2 in the
     reflected direction.
   - If it reaches the `Crate` first (no mirror involved), the character teleports straight
     there and wins immediately.
   - If it goes out of bounds or hits a `Tree` before reaching a mirror or the crate, `X` does
     nothing (no state change).

2. **Phase 2** — after bouncing off a mirror, the character travels *exactly the same number of
   cells* in the new direction as it did to reach the mirror (mirror-symmetric distance — like a
   reflection, the "distance in" equals the "distance out").
   - If the crate is reached at or before completing that distance, the character teleports there
     and wins.
   - If a wall or `Tree` blocks the path before completing that distance, `X` does nothing (no
     state change) — the character does *not* partially teleport.
   - If another mirror is hit along the way, it reflects again and continues, without resetting
     the distance budget.
   - If the full distance completes without obstruction, the character teleports to that cell
     (no win, just a repositioning).

This means a single mirror bounce won't necessarily land the character on the crate — extra
`W`/`A`/`S`/`D` moves may still be needed afterward, similar to the brief's own worked example
where `X` is followed by further movement (`D D D W`) to reach the target.

## Re-pressing `X` after teleporting
No dedicated "undo teleport" state is tracked. Pressing `X` again simply re-runs the same
two-phase simulation from wherever the character now is, facing whatever direction it's
currently facing.

## Mirror walkability
A character can walk onto a mirror's cell via `W`/`A`/`S`/`D` (only `Tree` blocks normal
movement) — this was an existing gap in the original logic, left as-is for time reasons. A
mirror only affects `X`'s projectile simulation, not footstep movement.

## Grid size
The sample world in `export.py` uses a 5x5 grid to
better demonstrate movement, a mirror bounce, and obstacles together in one run.
