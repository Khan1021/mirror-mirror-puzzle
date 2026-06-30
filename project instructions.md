# Mirror mirror

In this coding assignment, you will be building a puzzle game that can be distilled into a function that takes two inputs: configuration and movement instructions.

Your task is to write a function that returns the final state of the game and all intermediate steps taken to get there. A visualisation of this is required but it can use ASCII, symbols, emojis etc. The configuration input object can look however you wish.

The movement instructions can only contain a string with the following characters: "WASDX". TypeScript or Kotlin is preferable.

Like with real Software Engineering, sometimes the requirements are not clear and only examples are provided. If anything is unclear, document the assumptions you have made.

## Game World Construction Example
Visual examples in the document display the following:
* **Example 1 & 2:** Empty grid layouts (e.g., 3x2 and 5x5 grids) indicating the game is played on a 2D tile-based map.
* **Example 3:** A populated 5x5 grid containing:
  * A **character** (green hooded figure).
  * **Trees** (which appear to act as solid obstacles).
  * A **Mirror** (a circular, shield-like object angled diagonally).
  * A **Wooden Crate** (which appears to be the target or goal).

## Movement Instruction Examples
The character moves around the grid based on single-character string commands:
* `W`: Move Up
* `A`: Move Left
* `S`: Move Down
* `D`: Move Right

## Mirrors
The document demonstrates the use of the `X` command:
1. The character stands in alignment with a mirror.
2. Command `X` is executed.
3. The character shoots a glowing projectile forward.
4. The projectile travels until it hits the mirror, where it is reflected 90 degrees based on the mirror's orientation.

## Worked Example
A full sequence is shown visually on a grid with trees, a mirror, and a target crate:
* **Initial State:** Character starts at the bottom-left. Target crate is at the top-right.
* `A` 
* `D` 
* `W` 
* `W`
* `W` (Character positions themselves horizontally in line with the mirror)
* `X` (Character shoots a projectile; it travels right, hits the mirror, and reflects upwards towards the target)
* `D`
* `D`
* `D`
* `W` (Character walks over to the target crate)

*A reminder that your program will be passed two parameters: a world configuration object and an instructions string.*

---

## Guidelines
* **Time limit:** Spend 2-3 hours. Focus on building a working solution that demonstrates creativity and solid engineering.
* Do not over-engineer, be pragmatic.
* **Tools:** Use any language you wish. (Though TypeScript/Kotlin was noted as preferable earlier).
* If anything is unclear in this document, write an accompanying `Assumptions.md` document to accompany it.
* Upload a compressed file with your solution to the provided link by the specified date.

## Evaluation Criteria
1. **Correctness:** Does the code you have created align with the examples articulated above?
2. **Code quality:** Is the code clean, readable and maintainable?
3. **Extensibility:** Can the solution handle future changes?
4. **Testing:** Are key parts of the program tested?
