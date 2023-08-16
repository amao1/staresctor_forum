function sendVoteToServer(postID, userID, voteType) {
    const url = '/vote';
    const data = { postID, userID, voteType };
  
    fetch(url, {
      method: 'POST',
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
    const upvoteButtons = document.querySelectorAll('.upvote');
    const downvoteButtons = document.querySelectorAll('.downvote');
  
    function handleUpvoteClick(event) {
      const clickedUpvoteBtn = event.currentTarget;
      const parentContainer = clickedUpvoteBtn.closest('.d-flex');
      const postID = clickedUpvoteBtn.getAttribute('data-post-id');
      const userID = clickedUpvoteBtn.getAttribute('data-user-id');
      const upvote = 1;
      
      // Toggle the 'on' class for the clicked upvote button within its parent container
      clickedUpvoteBtn.classList.toggle('on');
  
      // Find the downvote button within the same parent container and remove the 'on' class if present
      const siblingDownvoteBtn = parentContainer.querySelector('.downvote');
      siblingDownvoteBtn.classList.remove('on');
  
      // Call the function to send the upvote to the server
      sendVoteToServer(postID, userID, upvote);
    }
  
    function handleDownvoteClick(event) {
      const clickedDownvoteBtn = event.currentTarget;
      const parentContainer = clickedDownvoteBtn.closest('.d-flex');
      const postID = clickedUpvoteBtn.getAttribute('data-post-id');
      const userID = clickedUpvoteBtn.getAttribute('data-user-id');
      const downvote = 1;
  
      // Toggle the 'on' class for the clicked downvote button within its parent container
      clickedDownvoteBtn.classList.toggle('on');
  
      // Find the upvote button within the same parent container and remove the 'on' class if present
      const siblingUpvoteBtn = parentContainer.querySelector('.upvote');
      siblingUpvoteBtn.classList.remove('on');
  
      // Call the function to send the downvote to the server
      sendVoteToServer(postID, userID, downvote);
    }
  
    upvoteButtons.forEach(btn => {
      btn.addEventListener('click', handleUpvoteClick);
    });
  
    downvoteButtons.forEach(btn => {
      btn.addEventListener('click', handleDownvoteClick);
    });
  });