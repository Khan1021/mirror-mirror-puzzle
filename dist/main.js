// helper function that converts single cell into an emoji
function cellToEmoji(cell) {
    if (cell == null) {
        return " ";
    }
    ;
    if (cell.type == "crate") {
        return "📦";
    }
    ;
    if (cell.type == "tree") {
        return "🌳";
    }
    ;
    if (cell.type == "mirror") {
        return "🪞";
    }
    ;
    if (cell.type == "character") {
        return "🧍";
    }
    ;
    return " ";
}
;
function renderGrid(state) {
    const rows = [];
    for (let y = 0; y < state.height; y++) {
        const rowSymbols = [];
        for (let x = 0; x < state.width; x++) {
            rowSymbols.push(cellToEmoji(state.grid[y][x]));
        }
        rows.push(rowSymbols.join(""));
    }
    return rows.join("\n");
}
const gridElement = document.getElementById("grid");
const statusElement = document.getElementById("status");
const prevButton = document.getElementById("prev");
const nextButton = document.getElementById("next");
let steps = [];
let currentStep = 0;
let won = false;
function showStep() {
    if (gridElement !== null) {
        gridElement.textContent = renderGrid(steps[currentStep]);
    }
    if (statusElement !== null) {
        const winText = won && currentStep === steps.length - 1 ? " — WON!" : "";
        statusElement.textContent = `Step ${currentStep + 1} / ${steps.length}${winText}`;
    }
}
if (prevButton !== null) {
    prevButton.addEventListener("click", () => {
        if (currentStep > 0) {
            currentStep -= 1;
            showStep();
        }
    });
}
if (nextButton !== null) {
    nextButton.addEventListener("click", () => {
        if (currentStep < steps.length - 1) {
            currentStep += 1;
            showStep();
        }
    });
}
fetch("game_data.json")
    .then((response) => response.json())
    .then((data) => {
    steps = data.steps;
    won = data.won;
    currentStep = 0;
    showStep();
});
export {};
//# sourceMappingURL=main.js.map