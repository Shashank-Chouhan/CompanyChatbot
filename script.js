document.addEventListener("DOMContentLoaded", function() {
    // Add event listener to the input field to detect "Enter" key press
    var userInputField = document.getElementById("user-input");
    userInputField.addEventListener("keydown", function(event) {
        if (event.key === "Enter") {
            sendMessage();
        }
    });
});

function sendMessage() {
    var userInput = document.getElementById("user-input").value;
    if (!userInput.trim()) {
        return; // If the input is empty or contains only whitespace, do nothing
    }
    displayMessage("You : " + userInput, true); // Display user's message in the chat
    document.getElementById("user-input").value = ""; // Clear input field

    // Send the user's message to the server
    fetch('http://127.0.0.1:8000/message', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: userInput }),
    })
    .then(response => response.json())
    .then(data => {
        var botResponse = data.message;
        displayMessage("Bot : "+botResponse, false); // Display bot's response in the chat
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

function displayMessage(message, isUser) {
    var chatMessages = document.getElementById("chat-messages");
    var messageElement = document.createElement("div");
    messageElement.classList.add("message");
    if (isUser) {
        messageElement.classList.add("user-message");
    } else {
        messageElement.classList.add("bot-message");
    }
    messageElement.innerText = message;
    chatMessages.appendChild(messageElement);
}
