from flask import Flask, request, render_template
from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

# Define the API endpoint for the backend
BACKEND_API_URL = "https://amulmm-brain-tumor-backend.hf.space"

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('index.html', prediction='No file part')
        file = request.files['file']
        if file.filename == '':
            return render_template('index.html', prediction='No selected file')
        if file:
            files = {'file': (file.filename, file.stream, file.content_type)}
            try:
                response = requests.post(f"{BACKEND_API_URL}/predict", files=files)
                response.raise_for_status() # Raise an exception for HTTP errors
                prediction_result = response.json()
                return render_template('index.html', prediction=f"Prediction: {prediction_result['prediction']} (Confidence: {prediction_result['confidence']})")
            except requests.exceptions.RequestException as e:
                return render_template('index.html', prediction=f'Error connecting to backend: {e}')
    return render_template('index.html', prediction=None)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5006))
    app.run(debug=True, host='0.0.0.0', port=port)