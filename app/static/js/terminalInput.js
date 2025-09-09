import {runSequentially, typeHtml} from './terminalWriteFx.js';

const cmdMap = {
    "/help":printHelp,
    "/give-hint":printHints,
    "unknownCommand":printError,
    "thisIsNotWhereYouTypeTheAnswer":wrongPlaceForAnswer
}

document.addEventListener('DOMContentLoaded', () => {
    const inputFields = document.querySelectorAll('.terminal-input');

    inputFields.forEach(input => {
        input.addEventListener('keydown', (event) => {
            if (event.key === 'Enter') {
                let command = input.value;
                let newCommand = null;
                if (!cmdMap.hasOwnProperty(command)) {newCommand = "unknownCommand";}
                if (commandHasURLRefs(command) === true){
                    newCommand = "thisIsNotWhereYouTypeTheAnswer";
                }
                if(newCommand !== null){command = newCommand}
                cmdMap[command]();
                input.value="";
            }
        });
    });
});

function wrongPlaceForAnswer(){
    const msgEl = createTerminalMsgEl("@ERROR", "It looks like you might try to write the answer in the terminal? It is pretty cool but... damn that addressbar in your browser looks PATHoligious.")
    sendNewTerminalMsg(msgEl);
}

function commandHasURLRefs(cmd){
    // Naive check to see if the user is attempting to write the answer in the terminal. 
    //source: https://stackoverflow.com/questions/6944744/javascript-get-portion-of-url-path
    const path = window.location.pathname;
    let checkFor = path.split("/")
    checkFor = checkFor.filter(item => item !== "");
    checkFor.push(path)
    checkFor.push(window.location.href)
    checkFor.push(window.location.domain)

    for (let i = 0; i < checkFor.length; i++) {
        const item = checkFor[i];
        if (cmd.includes(item)) {
            return true;
        }
    }
    return false;
}

function printError(){
    const msgEl = createTerminalMsgEl("@ERROR", "Unknown command. Type /help to see valid commands.")
    sendNewTerminalMsg(msgEl);
}

function printHints(){
    const hints = document.querySelectorAll(".hint.hidden");
    if (hints.length == 0){
        const noHintsMsg = createTerminalMsgEl("@hint", "Sorry, but I am out of hints.")
        sendNewTerminalMsg(noHintsMsg)
    }else {
        const nextHint = hints[0]
        if (nextHint.parentNode) {
            nextHint.parentNode.appendChild(nextHint);
        }
        nextHint.classList.remove("hidden");
        sendNewTerminalMsg(noHintsMsg)
        // runSequentially([nextHint], 0);
    }
}

function createTerminalMsgEl(author, msg){
    const newTerminalMsg = document.createElement("div");
    newTerminalMsg.appendChild(createAuthorTag(author));
    newTerminalMsg.append(":");
    newTerminalMsg.appendChild(createTildeEl());
    newTerminalMsg.appendChild(createMsgEl(msg));
    return newTerminalMsg;
}

function createAuthorTag(author){
    const authEl = document.createElement("span");
    authEl.classList.add("prompt");
    authEl.textContent = author;
    return authEl;
}

function createTildeEl(){
    const tildeEl = document.createElement("span");
    tildeEl.classList.add("u-text-pink");
    tildeEl.textContent="~";
    return tildeEl;
}

function createMsgEl(msg){
    const msgEl = document.createElement("code");
    msgEl.textContent = msg;
    return msgEl;
}

function sendNewTerminalMsg(terminalMsg){
    const terminalBody = document.getElementById("terminal-body");
    if (terminalBody === null){
        console.log("could not find terminal body");
        return;
    }
    terminalBody.appendChild(terminalMsg);
    //enqueueWriteTerminal(terminalMsg)
    runSequentially([terminalMsg],0);
}

function printHelp(){
    let commandsArray = Object.keys(cmdMap)
    commandsArray = commandsArray.filter(item => item.startsWith("/"))
    const commandsString = commandsArray.join(", ")
    const textContent = "Known commands: " + commandsString;
    const msg = createTerminalMsgEl("@help", textContent);
    sendNewTerminalMsg(msg);
}