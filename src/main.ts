interface Character{
    type:"character";
    direction: string;
}

interface Tree{
    type:"tree";
}

interface Mirror{
    type: "mirror";
    angle: number;
    
}

interface Crate{
    type: "crate";
}


type Cell = Character | Tree | Mirror | Crate| null;

interface GameState{
    width:number;
    height:number;
    grid:Cell[][];
}



const sampleState: GameState ={
    width: 3,
    height:3,
    grid:[
        [ {type: "character", direction: "right"},null, {type: "crate"}],
        [ null, {type: "mirror", angle: 45}, null ],
        [{type: "tree"}, null, {type: "tree"}]
    ]
};


// helper function that converts single cell into an emoji
function cellToEmoji(cell: Cell): string{
    if (cell==null){
        return " ";
    };
    if (cell.type == "crate"){
        return "📦";
    };
    if (cell.type=="tree"){
        return "🌳";
    };
    if (cell.type=="mirror"){
        return "🪞";
    };
    if (cell.type=="character"){
        return "🧍";
    };
    
    return " ";
};



function renderGrid(state: GameState): string{
    const rows:string[]=[];

    for(let y=0;y<state.height;y++){
        const rowSymbols:string[]=[];
        for (let x=0;x<state.width;x++){
            rowSymbols.push(cellToEmoji(state.grid[y]![x]!));
        }
        rows.push(rowSymbols.join(""));
    }
    return rows.join("\n");
}

const gridElement = document.getElementById("grid");
if (gridElement !== null) {
    gridElement.textContent = renderGrid(sampleState);
}