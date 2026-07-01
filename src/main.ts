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