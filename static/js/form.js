'use strict';

const form = document.querySelector('#greetings-form');
const recipient = document.querySelector('#recipient');
const message = document.querySelector('#message');
const recipientFeedback = document.querySelector('#recipient-feedback');
const messageFeedback = document.querySelector('#message-feedback');

form.addEventListener('submit', (e) => {
  if (recipient.value === '') {
    e.preventDefault();
    recipientFeedback.textContent = 'Please add a recipient';
  } else {
    recipientFeedback.textContent = '';
  }
  if (message.value === '') {
    e.preventDefault();
    messageFeedback.textContent = 'Please add a message';
  } else {
    messageFeedback.textContent = '';
  }
});
