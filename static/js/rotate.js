'use strict';
/* global XMLHttpRequest */

const recipient = document.querySelector('#recipient');
const message = document.querySelector('#message');
const next = document.querySelector('#next');
let currentGreeting = 0;
let allGreetings = [];

if (next) {
  next.addEventListener('click', nextGreeting);
}

function nextGreeting () {
  if (allGreetings.length > 0) {
    if (currentGreeting >= allGreetings.length) {
      currentGreeting = 0;
    }
    recipient.textContent = allGreetings[currentGreeting][1];
    message.textContent = allGreetings[currentGreeting][2];
    currentGreeting++;
  } else {
    next.disabled = true;
  }
}

const request = new XMLHttpRequest();

request.onload = function () {
  if (this.status === 200) {
    allGreetings = JSON.parse(this.response);
    if (allGreetings.length > 0) {
      next.disabled = false;
      nextGreeting();
    } else {
      next.disabled = true;
    }
  } else {
    console.error(`Request failed: ${this.status} ${this.statusText}`);
  }
};

request.onerror = function () {
  console.error('Request failed');
};

request.open('GET', '/greetings', true);
request.setRequestHeader('Accept', 'application/json');
request.send();
