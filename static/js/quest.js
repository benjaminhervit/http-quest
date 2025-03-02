'use strict'
document.addEventListener('DOMContentLoaded', function() {
    setInterval(function() {
        fetch('/all_teams')
            .then(response => response.json())
            .then(data => {
                const tbody = document.querySelector("#table_body");
                tbody.innerHTML = '';
                data.forEach(team => {
                    //create row
                    const row = document.createElement("tr");
                    tbody.appendChild(row);
                    
                    //team name
                    const grEl = document.createElement("th");
                    grEl.scope = "row";
                    grEl.textContent = team.team;
                    row.appendChild(grEl);

                    //level
                    const levelEl = document.createElement("td");
                    levelEl.textContent = team.score;
                    row.appendChild(levelEl);

                    //defeat the git
                    row.appendChild(createProgressBarGroupEl(team.score, 0, 2));
                    //open the gate
                    row.appendChild(createProgressBarGroupEl(team.score, 2, 5));
                    //claim the crown
                    row.appendChild(createProgressBarGroupEl(team.score, 5, 7));

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