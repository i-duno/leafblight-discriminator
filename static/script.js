const form = document.getElementById('uploadForm');
const fileInput = document.getElementById('fileInput');
const resultElement = document.getElementById('result');
const uploadedImage = document.getElementById('uploadedImage');
const predictionElement = document.getElementById('prediction');

form.addEventListener('submit', async (event) => {
    event.preventDefault();

    const file = fileInput.files[0];
    if (!file) {
        predictionElement.textContent = "Please select an image first.";
        return;
    }

    // lol heroku is slow didnt know what to expect anywho
    let dot_len = 0;
    let wait_text = "Classifying image"
    let wait_text_stack = ['So close yet so far', 'Almost there', 'Hold on a bit', 'Please wait']
    wait_id = setInterval(() => {
        switch (dot_len) {
            case 0:
                predictionElement.textContent = wait_text + '.'
                break;
            case 1:
                predictionElement.textContent = wait_text + '..'
                break;
            case 2:
                predictionElement.textContent = wait_text + '...'
                break;
        }
        dot_len++;
        if (dot_len >= 3) {
            dot_len = 0;
        }
    }, 350);
    long_time_id = setInterval(() => {
        if (wait_text_stack.length === 0) {return}
        wait_text = wait_text_stack.pop()
    }, 5000);

    // Display the uploaded image
    const reader = new FileReader()

    reader.onload = (e) => {
        uploadedImage.src = e.target.result;
    };
    reader.readAsDataURL(file);

    const formData = new FormData();
    formData.append("file", file);

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            body: formData
        });

        clearInterval(wait_id)
        clearInterval(long_time_id)

        if (response.ok) {
            const result = await response.json();
            console.log(result)
            predictionElement.textContent = `Prediction: ${result.class}, Confidence: ${result.confidence.toFixed(2)}%`;
        } else {
            predictionElement.textContent = "Error: Unable to get prediction.";
        }
    } catch (error) {

        clearInterval(wait_id)
        clearInterval(long_time_id)
        
        predictionElement.textContent = `Error: ${error.message}`;
    }
});