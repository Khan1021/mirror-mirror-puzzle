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


type Cell = Character | Tree | Mirror | Crate;