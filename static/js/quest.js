'use strict'
document.addEventListener('DOMContentLoaded', function() {
    updateLeaderBoard();
    setInterval(function() {
        updateLeaderBoard();
    }, 200000);
});

function updateLeaderBoard(){
    fetch('/all_teams')
            .then(response => response.json())
            .then(data => {
                console.log("Updating leaderboard")
                const tbody = document.querySelector("#table_body");
                tbody.innerHTML = '';
                data.forEach(team => {
                    //convert to JSON
                    const teamObj = JSON.parse(team);
                    //create row
                    const row = document.createElement("tr");
                    tbody.appendChild(row);
                    
                    //team name
                    const grEl = document.createElement("th");
                    grEl.textContent = teamObj.team;
                    row.appendChild(grEl);

                    //level
                    const levelEl = document.createElement("th");
                    levelEl.textContent = teamObj.exp;
                    row.appendChild(levelEl);

                    // TODO: MAKE SURE SCORE AND MAX VALUE MATCHES THE LEVELS
                    row.appendChild(createProgressBarGroupEl(teamObj.exp, 0, 5));
                    //open the gate
                    row.appendChild(createProgressBarGroupEl(teamObj.exp, 6, 8));
                    //claim the crown
                    row.appendChild(createProgressBarGroupEl(teamObj.exp, 8, 10));

                });

            })
            .catch(error => console.error('Error fetching teams:', error));
}

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