const sound = {
    65: "http://carolinegabriel.com/demo/js-keyboard/sounds/040.wav",
    87: "http://carolinegabriel.com/demo/js-keyboard/sounds/041.wav",
    83: "http://carolinegabriel.com/demo/js-keyboard/sounds/042.wav",
    69: "http://carolinegabriel.com/demo/js-keyboard/sounds/043.wav",
    68: "http://carolinegabriel.com/demo/js-keyboard/sounds/044.wav",
    70: "http://carolinegabriel.com/demo/js-keyboard/sounds/045.wav",
    84: "http://carolinegabriel.com/demo/js-keyboard/sounds/046.wav",
    71: "http://carolinegabriel.com/demo/js-keyboard/sounds/047.wav",
    89: "http://carolinegabriel.com/demo/js-keyboard/sounds/048.wav",
    72: "http://carolinegabriel.com/demo/js-keyboard/sounds/049.wav",
    85: "http://carolinegabriel.com/demo/js-keyboard/sounds/050.wav",
    74: "http://carolinegabriel.com/demo/js-keyboard/sounds/051.wav",
    75: "http://carolinegabriel.com/demo/js-keyboard/sounds/052.wav",
    79: "http://carolinegabriel.com/demo/js-keyboard/sounds/053.wav",
    76: "http://carolinegabriel.com/demo/js-keyboard/sounds/054.wav",
    80: "http://carolinegabriel.com/demo/js-keyboard/sounds/055.wav",
    186: "http://carolinegabriel.com/demo/js-keyboard/sounds/056.wav"
};


let combination = '';
var vol = true;



//Allows the user to play the piano with keyboard
//Handles the "Weeseeyou" key combination and plays separate sound
document.addEventListener("keydown", function(key) {
    const keys = [{
            keyCode: 65,
            id: "note-A",
            color: "grey",
            char: "a"
        },
        {
            keyCode: 87,
            id: "note-W",
            color: "grey",
            char: "w"
        },
        {
            keyCode: 83,
            id: "note-S",
            color: "grey",
            char: "s"
        },
        {
            keyCode: 69,
            id: "note-E",
            color: "grey",
            char: "e"
        },
        {
            keyCode: 68,
            id: "note-D",
            color: "grey",
            char: "d"
        },
        {
            keyCode: 70,
            id: "note-F",
            color: "grey",
            char: "f"
        },
        {
            keyCode: 84,
            id: "note-T",
            color: "grey",
            char: "t"
        },
        {
            keyCode: 71,
            id: "note-G",
            color: "grey",
            char: "g"
        },
        {
            keyCode: 89,
            id: "note-Y",
            color: "grey",
            char: "y"
        },
        {
            keyCode: 72,
            id: "note-H",
            color: "grey",
            char: "h"
        },
        {
            keyCode: 85,
            id: "note-U",
            color: "grey",
            char: "u"
        },
        {
            keyCode: 74,
            id: "note-J",
            color: "grey",
            char: "j"
        },
        {
            keyCode: 75,
            id: "note-K",
            color: "grey",
            char: "k"
        },
        {
            keyCode: 79,
            id: "note-OO",
            color: "grey",
            char: "o"
        },
        {
            keyCode: 76,
            id: "note-L",
            color: "grey",
            char: "l"
        },
        {
            keyCode: 80,
            id: "note-P",
            color: "grey",
            char: "p"
        },
        {
            keyCode: 186,
            id: "note-O",
            color: "grey",
            char: ";"
        }
    ];

    let currentKey = keys.find(k => k.keyCode === key.keyCode && vol);
    if (currentKey) {
        let {
            id,
            color,
            char
        } = currentKey;
        keyaudio = new Audio(sound[key.keyCode]);
        keyaudio.play();
        document.getElementById(id).style.backgroundColor = color;
        document.getElementById(id).style.transform = "scale(0.95)";
        if (char) combination += char;
    }
    if (combination.length >= 8) {
        let sign = combination.substring(combination.length - 8);
        if (sign === 'weseeyou' && vol) {
            keyaudio = new Audio('https://orangefreesounds.com/wp-content/uploads/2020/09/Creepy-piano-sound-effect.mp3?_=1');
            keyaudio.play();
            document.getElementById("piano-body").style.backgroundImage = "url('/static/main/images/texture.jpeg')"
            document.getElementById("keys").style.backgroundImage = "url('/static/main/images/texture.jpeg')";
            document.getElementById("keys").style.display = "none";
            document.getElementById("piano-text").innerHTML = "I have awoken!";
            console.log(sign);
            console.log(combination);
            vol = false;
        }
    }
});

//Reverts keys to intial state after being pressed
const pianoKeys = {
    65: {
        id: "note-A"
    },
    87: {
        id: "note-W"
    },
    83: {
        id: "note-S"
    },
    69: {
        id: "note-E"
    },
    68: {
        id: "note-D"
    },
    70: {
        id: "note-F"
    },
    84: {
        id: "note-T"
    },
    71: {
        id: "note-G"
    },
    89: {
        id: "note-Y"
    },
    72: {
        id: "note-H"
    },
    85: {
        id: "note-U"
    },
    74: {
        id: "note-J"
    },
    75: {
        id: "note-K"
    },
    79: {
        id: "note-OO"
    },
    76: {
        id: "note-L"
    },
    80: {
        id: "note-P"
    },
    186: {
        id: "note-O"
    }
};

document.addEventListener("keydown", function(key) {
    if (!pianoKeys[key.keyCode]) return;
    const {
        id
    } = pianoKeys[key.keyCode];
    document.getElementById(id).style.backgroundColor = white;
});

document.addEventListener("keyup", function(key) {
    if (!pianoKeys[key.keyCode]) return;
    const {
        id
    } = pianoKeys[key.keyCode];
    document.getElementById(id).style.backgroundColor = "";
    document.getElementById(id).style.transform = "";
});



//Allows the user to play the piano via mouse
function changeKeyAppearance(keyId, color, scale, sound) {
    document.getElementById(keyId).style.backgroundColor = color;
    document.getElementById(keyId).style.transform = `scale(${scale})`;
    if (sound) {
        let keyaudio = new Audio(sound);
        keyaudio.play();
    }
}



let key_a = document.getElementById("note-A");
key_a.addEventListener('mousedown', event => changeKeyAppearance("note-A", "grey", "0.9", sound[65]));
key_a.addEventListener('mouseup', event => changeKeyAppearance("note-A", "white", "1", ''));

let key_w = document.getElementById("note-W");
key_w.addEventListener('mousedown', event => changeKeyAppearance("note-W", "grey", "0.9", sound[87]));
key_w.addEventListener('mouseup', event => changeKeyAppearance("note-W", "black", "1", ''));

let key_s = document.getElementById("note-S");
key_s.addEventListener('mousedown', event => changeKeyAppearance("note-S", "grey", "0.9", sound[83]));
key_s.addEventListener('mouseup', event => changeKeyAppearance("note-S", "white", "1", ''));

let key_e = document.getElementById("note-E");
key_e.addEventListener('mousedown', event => changeKeyAppearance("note-E", "grey", "0.9", sound[69]));
key_e.addEventListener('mouseup', event => changeKeyAppearance("note-E", "black", "1", ''));

let key_d = document.getElementById("note-D");
key_d.addEventListener('mousedown', event => changeKeyAppearance("note-D", "grey", "0.9", sound[68]));
key_d.addEventListener('mouseup', event => changeKeyAppearance("note-D", "white", "1", ''));

let key_f = document.getElementById("note-F");
key_f.addEventListener('mousedown', event => changeKeyAppearance("note-F", "grey", "0.9", sound[70]));
key_f.addEventListener('mouseup', event => changeKeyAppearance("note-F", "white", "1", ''));

let key_t = document.getElementById("note-T");
key_t.addEventListener('mousedown', event => changeKeyAppearance("note-T", "grey", "0.9", sound[84]));
key_t.addEventListener('mouseup', event => changeKeyAppearance("note-T", "black", "1", ''));

let key_g = document.getElementById("note-G");
key_g.addEventListener('mousedown', event => changeKeyAppearance("note-G", "grey", "0.9", sound[71]));
key_g.addEventListener('mouseup', event => changeKeyAppearance("note-G", "white", "1", ''));

let key_y = document.getElementById("note-Y");
key_y.addEventListener('mousedown', event => changeKeyAppearance("note-Y", "grey", "0.9", sound[89]));
key_y.addEventListener('mouseup', event => changeKeyAppearance("note-Y", "black", "1", ''));

let key_h = document.getElementById("note-H");
key_h.addEventListener('mousedown', event => changeKeyAppearance("note-H", "grey", "0.9", sound[72]));
key_h.addEventListener('mouseup', event => changeKeyAppearance("note-H", "white", "1", ''));

let key_u = document.getElementById("note-U");
key_u.addEventListener('mousedown', event => changeKeyAppearance("note-U", "grey", "0.9", sound[85]));
key_u.addEventListener('mouseup', event => changeKeyAppearance("note-U", "black", "1", ''));

let key_j = document.getElementById("note-J");
key_j.addEventListener('mousedown', event => changeKeyAppearance("note-J", "grey", "0.9", sound[74]));
key_j.addEventListener('mouseup', event => changeKeyAppearance("note-J", "white", "1", ''));

let key_k = document.getElementById("note-K");
key_k.addEventListener('mousedown', event => changeKeyAppearance("note-K", "grey", "0.9", sound[75]));
key_k.addEventListener('mouseup', event => changeKeyAppearance("note-K", "white", "1", ''));

let key_oo = document.getElementById("note-OO");
key_oo.addEventListener('mousedown', event => changeKeyAppearance("note-OO", "grey", "0.9", sound[79]));
key_oo.addEventListener('mouseup', event => changeKeyAppearance("note-OO", "black", "1", ''));

let key_l = document.getElementById("note-L");
key_l.addEventListener('mousedown', event => changeKeyAppearance("note-L", "grey", "0.9", sound[76]));
key_l.addEventListener('mouseup', event => changeKeyAppearance("note-L", "white", "1", ''));

let key_p = document.getElementById("note-P");
key_p.addEventListener('mousedown', event => changeKeyAppearance("note-P", "grey", "0.9", sound[80]));
key_p.addEventListener('mouseup', event => changeKeyAppearance("note-P", "black", "1", ''));

let key_o = document.getElementById("note-O");
key_o.addEventListener('mousedown', event => changeKeyAppearance("note-O", "grey", "0.9", sound[186]));
key_o.addEventListener('mouseup', event => changeKeyAppearance("note-O", "white", "1", ''));