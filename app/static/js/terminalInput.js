import {runSequentially, typeHtml} from './terminalWriteFx.js';

const cmdMap = {
    "/help":printHelp,
    "/i-need-help":showHints
}

document.addEventListener('DOMContentLoaded', () => {
    const inputFields = document.querySelectorAll('.terminal-input');
    console.log(inputFields)

    inputFields.forEach(input => {
        input.addEventListener('keydown', (event) => {
            if (event.key === 'Enter') {
                const command = input.value;
                if (!cmdMap.hasOwnProperty(command)) {
                    input.placeholder = "ERROR: Unknown command. Try /help.";
                } else {
                    input.placeholder = "Write commands. Type /help to see valid commands.";
                    cmdMap[command]();
                }
                input.value="";
            }
        });
    });
});

function showHints(){
    const hints = Array.from(document.querySelectorAll(".hint"));
    hints.forEach(hint => {
        if (hint.parentNode) {
            hint.parentNode.appendChild(hint);
        }
        hint.classList.remove("hidden");
    });
    runSequentially(hints, 0, 15);
}

function printHelp(){
    const terminalBody = document.getElementById("terminal-body");
    if (terminalBody === null){
        console.log("could not find terminal body");
        return;
    }

    const div = createFromTag("@help")
    const code = document.createElement("code");
    const commands = Object.keys(cmdMap).join(', ');
    code.textContent = "Known commands: " + commands;
    div.appendChild(code);
    terminalBody.appendChild(div);
}

function createFromTag(tag){
    //target element below
    //<div><span class="prompt">@story</span>:<span class="u-text-pink">~</span><code>{{content.story}}</code> </div>

    const div = document.createElement("div");
    //@tag
    const tagSpan = document.createElement("span");
    tagSpan.classList.add("prompt");
    tagSpan.textContent = tag;
    div.appendChild(tagSpan);

    //:
    div.content+=":";
    
    //~
    const squiggleSpan = document.createElement("span");
    squiggleSpan.classList.add("u-text-pink");
    squiggleSpan.textContent="~";
    div.appendChild(squiggleSpan);

    //text
    return div;
}