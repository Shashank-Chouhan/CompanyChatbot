document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the form from submitting normally

    // Get the form data
    const formData = new FormData(event.target);

    // Convert the form data to a JSON object
    const jsonObject = {};
    formData.forEach(function(value, key){
        jsonObject[key] = value;
    });

    // Send a POST request to the API endpoint
    fetch('http://127.0.0.1:8000/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(jsonObject),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        // Handle the response from the server
        console.log(data);
        if (data.message == 'success'){
            window.location.href = '../adminpageComponent/adminpage.html';
        }else {
            // Display error message if authentication fails
            alert('Invalid username or password');
        }
        
        // You can redirect the user or perform any other action based on the response
    })
    .catch(error => {
        console.error('There was a problem with your fetch operation:', error);
    });
});