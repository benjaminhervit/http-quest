'use strict';
/* global XMLHttpRequest */
const deleteButtons = document.querySelectorAll('.delete');
const greetings = document.querySelector('#greetings');

function deleteThisGreetingOnServer(e) {
  const id = e.target.attributes['data-id'].value;
  const requestURL = `${document.URL}/${id}`;
  const request = new XMLHttpRequest();
  request.addEventListener('load', function () {
    deleteThisGreetingOnPage(id);
  });

  deleteThisGreetingOnPage(id);
  request.open('DELETE', requestURL, true);
  request.send();
}

function deleteThisGreetingOnPage(id) {
  print("SO FAR SO GOOD!");
  const selector = `#greeting-${id}`;
  const theGreeting = document.querySelector(selector);

  if (theGreeting) {
    greetings.removeChild(theGreeting);
    const requestURL = `/test_page`;
    const request = new XMLHttpRequest();
    request.open('GET', requestURL, true);
  } else {
    console.error('Trying to delete the deleted', selector, theGreeting);
  }
}

if (deleteButtons) {
  for (const myButton of deleteButtons) {
    myButton.addEventListener('click', deleteThisGreetingOnServer);
  }
}
