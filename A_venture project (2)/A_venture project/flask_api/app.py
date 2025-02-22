from flask import Flask, request, jsonify
import joblib
import pandas as pd
from werkzeug.utils import secure_filename
import os
import logging
from sentence_transformers import SentenceTransformer
import numpy as np

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Load the classifier model
try:
    model = joblib.load('flask_api/activity_classifier.pkl')
    logging.info("Classifier model loaded successfully.")
except Exception as e:
    logging.error(f"Error loading classifier: {e}")
    exit()

# Load the SentenceTransformer model
try:
    model_name = 'all-mpnet-base-v2'  # Or another suitable model name from Hugging Face Hub
    vectorizer = SentenceTransformer(model_name)
    logging.info(f"SentenceTransformer model '{model_name}' loaded successfully.")
except Exception as e:
    logging.error(f"Error loading SentenceTransformer: {e}")
    exit()

@app.route("/")
def home():
    return "Welcome to the Activity Classifier API!"

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json  # Expecting {"text": "Some activity suggestion"}
        text = data.get("text", "")

        if not text:
            return jsonify({"error": "No text provided"}), 400

        transformed_text = vectorizer.encode([text])  # Use encode()
        logging.debug(f"Transformed text: {transformed_text}")

        if isinstance(transformed_text, np.ndarray):  # Check if it is a NumPy array
            transformed_text_reduced = transformed_text[:, :384]  # Select the first 384 features
            prediction = model.predict(transformed_text_reduced)
            return jsonify({"prediction": prediction.tolist()})
        else:
            logging.error("transformed_text is not a NumPy array")
            return jsonify({"error": "Internal error"}), 500

    except Exception as e:
        logging.error(f"Error in /predict: {e}")
        return jsonify({"error": f"An error occurred: {e}"}), 500

@app.route("/upload", methods=["POST"])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            # Check if the 'uploads' directory exists; create it if not
            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                os.makedirs(app.config['UPLOAD_FOLDER'])

            file.save(filepath)

            df = pd.read_excel(filepath)
            descriptions = df['description'].tolist()
            logging.debug(f"Descriptions: {descriptions}")

            transformed_descriptions = vectorizer.encode(descriptions)
            logging.debug(f"Type of transformed_descriptions: {type(transformed_descriptions)}")
            logging.debug(f"Transformed descriptions: {transformed_descriptions}")

            if isinstance(transformed_descriptions, np.ndarray):  # Check if it is a NumPy array
                transformed_descriptions_reduced = transformed_descriptions[:, :384]  # Select the first 384 features
                predictions = model.predict(transformed_descriptions_reduced)
                df['predicted_label'] = predictions.tolist()  # Convert predictions to list
            else:
                logging.error("transformed_descriptions is not a NumPy array")
                return jsonify({"error": "Internal error"}), 500

            output_filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'predictions.xlsx')
            df.to_excel(output_filepath, index=False)

            logging.info(f"File processed successfully. Predictions saved to: {output_filepath}")
            return jsonify({"message": "File processed successfully", "output_file": output_filepath}), 200

    except Exception as e:
        logging.error(f"Error in /upload: {e}")
        return jsonify({"error": f"An error occurred: {e}"}), 500

    return jsonify({"error": "Invalid request"}), 400  # Should not be reached

if __name__ == "__main__":
    app.run(port=5000, debug=True)