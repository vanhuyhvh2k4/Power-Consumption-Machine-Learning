document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form');
    const resultDiv = document.querySelector('.result');
    const historyList = document.getElementById('history-list');
    const clearHistoryButton = document.getElementById('clear-history');

    if (!resultDiv) {
        console.error('Result div not found in the DOM. Ensure the .result element exists in the HTML.');
        return;
    }

    // Load prediction history
    const history = JSON.parse(localStorage.getItem('prediction_history')) || [];

    // Ensure history is initialized in localStorage
    if (!localStorage.getItem('prediction_history')) {
        localStorage.setItem('prediction_history', JSON.stringify(history));
    }

    history.forEach(item => {
        const li = document.createElement('li');
        li.textContent = item;
        historyList.insertBefore(li, historyList.firstChild); // Insert at the top
    });

    // Save values and update history on form submit
    form.addEventListener('submit', function (event) {
        event.preventDefault(); // Prevent default form submission

        const formData = new FormData(form);
        fetch('/', {
            method: 'POST',
            body: formData
        })
        .then(response => response.text())
        .then(html => {
            // Parse the returned HTML to extract the prediction text
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');
            const resultElement = doc.querySelector('.result');
            if (resultElement) {
                const newResult = resultElement.textContent;

                // Update the result div
                if (resultDiv) {
                    resultDiv.textContent = newResult;

                    // Update history
                    const newEntry = `${new Date().toLocaleString()}: ${newResult}`;
                    history.unshift(newEntry); // Add new entry to the beginning
                    localStorage.setItem('prediction_history', JSON.stringify(history));

                    const li = document.createElement('li');
                    li.textContent = newEntry;
                    historyList.insertBefore(li, historyList.firstChild); // Insert at the top
                } else {
                    console.error('Result div not found in the DOM.');
                }
            } else {
                console.error('Result element not found in the returned HTML.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });

    // Clear history
    clearHistoryButton.addEventListener('click', function () {
        localStorage.removeItem('prediction_history');
        historyList.innerHTML = '';
    });
});
