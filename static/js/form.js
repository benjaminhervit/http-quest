'use strict';

const form = document.querySelector('#register-form');
const recipient = document.querySelector('#recipient');
const message = document.querySelector('#message');
const recipientFeedback = document.querySelector('#recipient-feedback');
const messageFeedback = document.querySelector('#message-feedback');

const gameContext = document.querySelector("#game-context")

form.addEventListener('submit', (e) => {
  e.preventDefault();
  const team = document.querySelector('#team');
  const gameFeedback = document.querySelector('#game-feedback');
  if (team.value === '') {
    gameFeedback.textContent = 'Please add a team';
    return;
  } 

  const requestURL = `${document.URL}/${id}`;
  const request = new XMLHttpRequest();
  request.addEventListener('load', function () {
    if (request.status >= 200 && request.status < 300) {
      const responseData = JSON.parse(request.responseText);
      if (responseData.success) {
        gameFeedback.textContent = responseData.message;
      } else {
        gameFeedback.textContent = responseData.error;
      }
    } else {
      gameFeedback.textContent = 'Failed to submit. Please try again.';
    }
  });
  request.open('POST', requestURL, true);
  request.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');
  const formData = new FormData(form);
  request.send(formData);
});
