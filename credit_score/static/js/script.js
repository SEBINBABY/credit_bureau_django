let questions = []; // Array to store questions fetched from the API
let currentQuestionIndex = 0; // Track current question index
let responses = []; // Array to store user responses

// Function to open the popup modal
function openPopup() {
  document.getElementById('popupModal').style.display = 'flex';
  fetchQuestions(); // Fetch questions when the modal is opened
}

// Function to close the popup modal
function closePopup() {
  document.getElementById('popupModal').style.display = 'none';
  currentQuestionIndex = 0; // Reset the question index
  responses = []; // Reset responses
  document.getElementById('progressFill').style.width = '0%'; // Reset progress bar
}

// Function to fetch questions from the server 
function fetchQuestions() {
  fetch('/api/questions/')
    .then(response => response.json())
    .then(data => {
      questions = data.map(q => ({
      id: q.id,
      text: q.question_text,
      options: [q.answer_a, q.answer_b, q.answer_c, q.answer_d]
      }))
      displayQuestion();
    });
}

// Function to display the current question
function displayQuestion() {
  if (currentQuestionIndex < questions.length) {
    const question = questions[currentQuestionIndex];
    document.getElementById('questionContainer').innerHTML = `
      <p><strong>${question.text}</strong></p>
      ${question.options.map(option => `
        <label>
          <input type="radio" name="response" value="${option}"> ${option}
        </label><br><br>
      `).join('')}
    `;
    updateProgressBar(); // Update progress bar with each question
  } else {
    alert("You can submit the assessment now");
  }
}

// Function to handle the "Next" button
function nextQuestion() {
  const selectedOption = document.querySelector('input[name="response"]:checked');
  if (selectedOption) {
    const selectedAnswer = selectedOption.value;
    const currentQuestion = questions[currentQuestionIndex]
    // Push the response to the responses array
    responses.push({
      question_id: currentQuestion.id,
      answer: selectedAnswer,
      user_id: currentUserId  // Attached user ID dynamically
    });
    currentQuestionIndex++;
    displayQuestion(); // Display the next question
  } else {
    alert("Please select an answer.");
  }
}



// Function to update the progress bar
function updateProgressBar() {
  const progressPercent = ((currentQuestionIndex + 1) / questions.length) * 100;
  document.getElementById('progressFill').style.width = progressPercent + '%';
}

// Function to submit responses to the backend
function submitResponses() {
  fetch('/api/save_response/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCsrfToken()
    },
    body: JSON.stringify({ responses: responses})  // Send all responses at once
  })
  .then(response => {
    console.log('Status Code:', response.status);  // Check the status code
    return response.json();
  })
  .then(result => {
    if (result.success) {
      alert('All responses saved successfully!');
      closePopup();  // Close the popup 
    } else {
      alert('Failed to save responses');
    }
  })
  .catch(error => console.error('Error:', error));
}

// Helper function to retrieve the CSRF token
function getCsrfToken() {
  const csrfTokenElement = document.querySelector('[name=csrfmiddlewaretoken]');
  if (!csrfTokenElement) {
    console.error('CSRF token element not found!');
    return '';  // Return an empty string or handle the error
  }
  return csrfTokenElement.value;
}