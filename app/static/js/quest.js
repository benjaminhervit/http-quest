'use strict'
let leaderboard;
let timer = null;
let controller = null; // optional, for pause/visibility
const interval = 5000;

document.addEventListener('DOMContentLoaded', function() {
    leaderboard = document.querySelector("#table_body");
    startLoop();
    document.addEventListener('visibilitychange', onVisChange)
    // updateLeaderBoard();
    // setInterval(function() {
    //     updateLeaderBoard();
    // }, 5000);
});

function onVisChange(){
    if (document.hidden) pauseLoop();
    else startLoop();
}

function startLoop(){
    if (timer || document.hidden) return;
    loopTick();
}

function pauseLoop(){
    if (timer){
        clearTimeout(timer);
        timer = null;
    }

    if (controller){
        controller.abort();
        controller = null;
    }
}

function loopTick(){
    if (!leaderboard || document.hidden) return;

    controller = new AbortController();

    fetch('/api/all_users', {
        headers: {Accept: 'application/json'},
        signal: controller.signal
    })
    .then((res)=>{
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json()
    })
    .then(renderLeaderboard)
    .catch((err)=>{
        if (err.name !== 'AbortError') console.log("Fetch users failed: ", err)
    })
    .finally(()=>{
        controller = null;
        if(!document.hidden) timer = setTimeout(loopTick, interval);
    })
}

function renderLeaderboard(data){
    if (!Array.isArray(data)) return;

    //console.log("Updating leaderboard")
    leaderboard.innerHTML = '';
    data.forEach(user => {
        //create row
        const row = document.createElement("tr");
        leaderboard.appendChild(row);
        
        //team name
        const userEl = document.createElement("td");
        userEl.textContent = user.username;
        row.appendChild(userEl);

        // //level
        const xpEL = document.createElement("td");
        xpEL.textContent = user.xp;
        row.appendChild(xpEL);

        // TODO: MAKE SURE SCORE AND MAX VALUE MATCHES THE LEVELS
        row.appendChild(createProgressBarGroupEl(user.xp, 0, 4));
        //open the gate
        row.appendChild(createProgressBarGroupEl(user.xp, 4, 8));
        //claim the crown
        row.appendChild(createProgressBarGroupEl(user.xp, 8, 10));

    });
}

// function updateLeaderBoard(){
//     if (leaderboard === null){
//         console.log("no leaderboard found. Update aborted.");
//         return;
//     }

//     fetch('/api/all_users')
//             .then(response => {
//                 if (!response.ok) throw new Error(`HTTP ${response.status}`);
//                 return response.json();
//             })
//             .then(data => {
//                 //console.log("Updating leaderboard")
//                 leaderboard.innerHTML = '';
//                 data.forEach(user => {
//                     //create row
//                     const row = document.createElement("tr");
//                     leaderboard.appendChild(row);
                    
//                     //team name
//                     const userEl = document.createElement("td");
//                     userEl.textContent = user.username;
//                     row.appendChild(userEl);

//                     // //level
//                     const xpEL = document.createElement("td");
//                     xpEL.textContent = user.xp;
//                     row.appendChild(xpEL);

//                     // TODO: MAKE SURE SCORE AND MAX VALUE MATCHES THE LEVELS
//                     row.appendChild(createProgressBarGroupEl(user.xp, 0, 4));
//                     //open the gate
//                     row.appendChild(createProgressBarGroupEl(user.xp, 4, 8));
//                     //claim the crown
//                     row.appendChild(createProgressBarGroupEl(user.xp, 8, 10));

//                 });

//             })
//             .catch(error => console.error('Error fetching user:', error));
// }

function createProgressBarGroupEl(exp, treshold, max){
    const divEl = document.createElement('td');
    const progEl = document.createElement('progress');
    progEl.max = max;
    if (exp <= treshold){
        progEl.value = 0;
    }
    else {
        progEl.value = exp;
    }
    divEl.appendChild(progEl);
    return divEl;
}