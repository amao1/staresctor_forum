function sendVoteToServer(targetID, userID, voteType, targetType) {
  const url = '/vote';
  const data = { 
    targetID: targetID,
    userID: userID,
    voteType: voteType,
    targetType: targetType
  }; 

  fetch(url, {
    method: "POST",
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  })
    .then(response => response.json())
    .then(data => {
      // Handle the response from the server if needed
      console.log(data);
    })
    .catch(error => {
      // Handle errors if necessary
      console.error('Error:', error);
    });
}

document.addEventListener('DOMContentLoaded', function () {
  const voteButtons = document.querySelectorAll('.upvote, .downvote');

  function handleVoteClick(event) {
    const clickedVoteBtn = event.currentTarget;
    const parentContainer = clickedVoteBtn.closest('.d-flex');
    const targetID = clickedVoteBtn.getAttribute('data-target-id');
    const userID = clickedVoteBtn.getAttribute('data-user-id');
    const voteType = clickedVoteBtn.classList.contains('upvote') ? 1 : -1;
    const targetType = clickedVoteBtn.classList.contains('post-vote') ? 'post' : 'comment';

    // Toggle the 'on' class for the clicked vote button within its parent container
    clickedVoteBtn.classList.toggle('on');

    // Find the other vote button within the same parent container and remove the 'on' class if present
    const siblingVoteBtn = parentContainer.querySelector('.upvote, .downvote');
    siblingVoteBtn !== clickedVoteBtn && siblingVoteBtn.classList.remove('on');

    // Call the function to send the vote to the server
    sendVoteToServer(targetID, userID, voteType, targetType);
  }

  voteButtons.forEach(btn => {
    btn.addEventListener('click', handleVoteClick);
  });
});