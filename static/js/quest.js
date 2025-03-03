'use strict'
document.addEventListener('DOMContentLoaded', function() {
    setInterval(function() {
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
                    levelEl.textContent = teamObj.score;
                    row.appendChild(levelEl);

                    row.appendChild(createProgressBarGroupEl(teamObj.score, 0, 2));
                    //open the gate
                    row.appendChild(createProgressBarGroupEl(teamObj.score, 2, 5));
                    //claim the crown
                    row.appendChild(createProgressBarGroupEl(teamObj.score, 5, 7));

                });

            })
            .catch(error => console.error('Error fetching teams:', error));
    }, 5000);
});

function createProgressBarGroupEl(score, treshold, max){
    const divEl = document.createElement('td');
    const progEl = document.createElement('progress');
    if(score > treshold){
        progEl.value = score;
        progEl.max = max;
    }
    divEl.appendChild(progEl);
    return divEl;
}