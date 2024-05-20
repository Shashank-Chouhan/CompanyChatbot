function logout() {
    alert("Logged out successfully.")
}

function uploadFile() {
    var fileInput = document.getElementById('fileInput');
    var file = fileInput.files[0];
    if (!file) {
        alert('Please select a file.');
        return;
    }
    if(file.name.slice(-4) != '.pdf'){
        alert('Please select a pdf file.')
        return;
    }
    var formData = new FormData();
    formData.append('file', file);

    fetch('http://localhost:8000/fileupload', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (response.ok) {
            alert('File uploaded successfully!');
            // x = total_files += 1
            // alert(x + ' files uploaded successfully')
        } else {
            alert('Error uploading file.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error uploading file.');
    });
}

function createdb() {
    var overlay = document.getElementById('overlay');
    var overlayMessage = document.getElementById('overlay-message');
    overlay.style.display = 'block'; // Show the overlay
    overlayMessage.innerHTML = '<p>Please wait, creating database...</p><i class="fas fa-spinner spinner"></i>'; // Show loading message
    overlay.classList.add('show-spinner'); // Add class to show spinner

    fetch('http://localhost:8000/createdb', {
        method: 'GET'
    })
    .then(response => {
        if (response.ok) {
            alert('Database created successfully!');
            return response.json();
        } else {
            alert('Error creating database.');
        }
    })
    .then(data => {
        console.log('Response:', data);
        console.log(data.message);
        overlay.style.display = 'none'; // Hide the overlay when response received
   
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error creating database.');
        overlay.style.display = 'none'; // Hide the overlay on error too

    });
}


function showdb() {
    var overlay = document.getElementById('overlay');
    var overlayMessage = document.getElementById('overlay-message');
    overlay.style.display = 'block'; // Show the overlay
    overlayMessage.innerText = 'Please wait, fetching data from database...'; // Show loading message

    fetch('http://localhost:8000/showdb', {
        method: 'GET'
    })
    .then(response => {
        if (response.ok) {
            return response.json(); // Assuming the API returns JSON
        } else {
            throw new Error('Error fetching data from database.');
        }
    })
    .then(data => {
        console.log(data)
        var dataDisplay = document.getElementById('dataDisplay');
        dataDisplay.innerHTML = '<h3>Data from Database:</h3>';

        data.forEach((item, index) => {
            var [id, question, answer] = item;
            var colorClass = index % 2 === 0 ? 'box-lightblue' : 'box-lightgreen';

            var box = document.createElement('div');
            box.className = `box ${colorClass}`;
            box.id = `box-${id}`;

            var qElement = document.createElement('p');
            qElement.innerHTML = `<strong>Q${index + 1}: ${question}</strong>`;
            box.appendChild(qElement);

            var aElement = document.createElement('p');
            aElement.innerHTML = `<strong>A${index + 1}: ${answer}</strong>`;
            box.appendChild(aElement);

            var buttonContainer = document.createElement('div');
            buttonContainer.className = 'button-container';

            var editButton = document.createElement('button');
            editButton.className = 'icon-button';
            editButton.innerHTML = '<i class="fas fa-edit"></i>';
            editButton.onclick = function() {
                editQA(id, question, answer); // Use the ID to handle editing
            };

            var deleteButton = document.createElement('button');
            deleteButton.className = 'icon-button';
            deleteButton.innerHTML = '<i class="fas fa-trash"></i>';
            deleteButton.onclick = function() {
                deleteQA(id); // Use the ID to handle deletion
            };

            buttonContainer.appendChild(editButton);
            buttonContainer.appendChild(deleteButton);
            box.appendChild(buttonContainer);

            dataDisplay.appendChild(box);
        });

        overlay.style.display = 'none'; // Hide the overlay when response received
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error fetching data from database.');
        overlay.style.display = 'none'; // Hide the overlay on error too
    });
}

function editQA(id, question, answer) {
    var box = document.getElementById(`box-${id}`);
    box.innerHTML = `
        <p><strong>Edit Question:</strong></p>
        <input type="text" id="edit-question-${id}" value="${question}" />
        <p><strong>Edit Answer:</strong></p>
        <input type="text" id="edit-answer-${id}" value="${answer}" />
        <div class="button-container">
            <button class="icon-button " onclick="submitEdit(${id})">Submit</button>
            <button class="icon-button " onclick="cancelEdit(${id}, '${question}', '${answer}')">Cancel</button>
        </div>
    `;
}

function submitEdit(id) {
    var editedQuestion = document.getElementById(`edit-question-${id}`).value;
    var editedAnswer = document.getElementById(`edit-answer-${id}`).value;

    fetch('http://localhost:8000/editquestion', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            id: id,
            question: editedQuestion,
            answer: editedAnswer
        })
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error('Error editing question.');
        }
    })
    .then(data => {
        showdb(); // Refresh the data display
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error editing question.');
    });
}

function cancelEdit(id, question, answer) {
    var box = document.getElementById(`box-${id}`);
    var index = id - 1; // Assuming ID starts from 1 and corresponds to index

    var colorClass = index % 2 === 0 ? 'box-lightblue' : 'box-lightgreen';
    box.className = `box ${colorClass}`;
    box.innerHTML = `
        <p><strong>Q${id}: ${question}</strong></p>
        <p><strong>A${id}: ${answer}</strong></p>
        <div class="button-container">
            <button class="icon-button" onclick="editQA(${id}, '${question}', '${answer}')"><i class="fas fa-edit"></i></button>
            <button class="icon-button" onclick="deleteQA(${id})"><i class="fas fa-trash"></i></button>
        </div>
    `;
}

function deleteQA(id) {
    var confirmation = confirm("Are you sure you want to delete this QA pair?");
    if (!confirmation) {
        return;
    }

    fetch(`http://localhost:8000/deletequestion/${id}`, {
        method: 'DELETE'
    })
    .then(response => {
        if (response.ok) {
            alert('QA pair deleted successfully!');
            // showdb(); // Refresh the data display
        } else {
            throw new Error('Error deleting QA pair.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error deleting QA pair.');
    });
}

function deleteWholeDB() {
    // First confirmation
    var firstConfirmation = confirm("WARNING: Are you sure you want to delete the entire database? This action cannot be undone.");
    if (!firstConfirmation) {
        console.log('Cancelled');
        return;
    }

    // Second confirmation
    var secondConfirmation = confirm("This is your second and final warning: Are you absolutely sure you want to delete the entire database?");
    if (!secondConfirmation) {
        console.log('Cancelled');
        return;
    }

    // If both confirmations are true, make the API call
    fetch('http://localhost:8000/deleteWholeDB', {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        console.log(response)
        if (response.ok) {
            alert('Entire database deleted successfully!');
            showdb(); // Optionally refresh the data display if needed
        } else {
            throw new Error('Error deleting the entire database.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error deleting the entire database.');
    });
}


function addQAPair() {
    var dataDisplay = document.getElementById('dataDisplay');

    var newBox = document.createElement('div');
    newBox.className = 'box box-lightblue'; // Set the default box color
    newBox.innerHTML = `
        <p><strong>Enter Question:</strong></p>
        <input type="text" class="qa-input" placeholder="Enter your question">
        <p><strong>Enter Answer:</strong></p>
        <input type="text" class="qa-input" placeholder="Enter your answer">
        <div class="button-container">
            <button class="icon-button" onclick="submitNewQA(this.parentElement.parentElement)">Submit</button>
            <button class="icon-button" onclick="cancelAddQAPair(this.parentElement.parentElement)">Cancel</button>
        </div>
    `;

    dataDisplay.appendChild(newBox);
    window.scrollTo(0, document.body.scrollHeight);
}

function submitNewQA(box) {
    var questionInput = box.querySelectorAll('input')[0];
    var answerInput = box.querySelectorAll('input')[1];

    var question = questionInput.value.trim();
    var answer = answerInput.value.trim();
    if (question === '' || answer === '') {
        alert('Please enter both question and answer.');
        return;
    }

    fetch('http://localhost:8000/addQAPair', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            question: question,
            answer: answer
        })
    })
    .then(response => {
        if (response.ok) {
            alert('QA pair added successfully!');
            // showdb(); // Refresh the data display
        } else {
            throw new Error('Error adding QA pair.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error adding QA pair.');
    });
}

function cancelAddQAPair(box) {
    box.parentNode.removeChild(box); // Remove the new box if canceled
}
