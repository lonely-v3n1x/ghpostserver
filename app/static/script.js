document.addEventListener('DOMContentLoaded', () => {
    const getLocationForm = document.getElementById('get-location-form');
    const getAddressForm = document.getElementById('get-address-form');
    const resultElement = document.getElementById('result');

    const apiBaseUrl = '/api';

    const displayError = (message) => {
        resultElement.innerHTML = `<p style="color: red;">Error: ${message}</p>`;
    };

    const displayResult = (data) => {
        try {
            // The actual response is a JSON string within the 'response' field
            const responseData = JSON.parse(data.response);
            let output = '';

            if (responseData.Table && responseData.Table.length > 0) {
                const details = responseData.Table[0];
                
                // Define which fields are relevant and their display order
                const relevantFields = ['GPSName', 'District', 'Street', 'Area', 'Town', 'Community','Region', 'PostalArea','PostCode'];
                const locationFields = ['CenterLatitude', 'CenterLongitude'];

                output += `<h3>Result Details:</h3>`;
                output += `<ul>`;

                // Display relevant fields first
                relevantFields.forEach(key => {
                    if (details[key]) {
                        const formattedKey = key === 'GPSName' ? 'Digital Address' : key.replace(/([A-Z])/g, ' $1').trim();
                        output += `<li><strong>${formattedKey}:</strong> ${details[key]}</li>`;
                    }
                });

                // Display Latitude and Longitude last
                locationFields.forEach(key => {
                    if (details[key]) {
                        const formattedKey = key.replace(/([A-Z])/g, ' $1').trim();
                        output += `<li><strong>${formattedKey}:</strong> ${details[key]}</li>`;
                    }
                });

                output += `</ul>`;
            } else if (responseData.ResponseMessage) {
                 output = `<p>${responseData.ResponseMessage}</p>`;
            } 
            else {
                output = `<p>No results found.</p>`;
            }
            resultElement.innerHTML = output;
        } catch (e) {
            // If parsing fails, display the raw response
            resultElement.textContent = data.response || 'Could not parse the response from the server.';
        }
    };

    getLocationForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const digitalAddress = document.getElementById('digital-address').value;
        resultElement.textContent = 'Loading...';

        try {
            const response = await fetch(`${apiBaseUrl}/get_location`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ code: digitalAddress }),
            });
            const data = await response.json();
            if (response.ok) {
                displayResult(data);
            } else {
                displayError(data.error || 'An unknown error occurred.');
            }
        } catch (error) {
            displayError(error.message);
        }
    });

    getAddressForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const latitude = document.getElementById('latitude').value;
        const longitude = document.getElementById('longitude').value;
        resultElement.textContent = 'Loading...';

        try {
            const response = await fetch(`${apiBaseUrl}/get_address`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ latitude, longitude }),
            });
            const data = await response.json();
            if (response.ok) {
                displayResult(data);
            } else {
                displayError(data.error || 'An unknown error occurred.');
            }
        } catch (error) {
            displayError(error.message);
        }
    });
});
