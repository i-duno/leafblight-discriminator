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

        if (response.ok) {
            const result = await response.json();
            console.log(result)
            predictionElement.textContent = `Prediction: ${result.class}, Confidence: ${result.confidence.toFixed(2)}%`;
        } else {
            predictionElement.textContent = "Error: Unable to get prediction.";
        }
    } catch (error) {
        predictionElement.textContent = `Error: ${error.message}`;
    }
});