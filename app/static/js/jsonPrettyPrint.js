document.addEventListener("DOMContentLoaded", () => {
    const preEl = document.getElementById("json");
    console.log(preEl)
    const json = preEl.textContent;
    preEl.textContent = JSON.stringify(JSON.parse(json), undefined, 2);
});