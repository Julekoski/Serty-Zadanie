# app.py

import os
import requests
import io  
from flask import Flask, request, jsonify
from flask_cors import CORS
from validation import validate_pdf_file
import pypdf
from dotenv import load_dotenv

# Load env
load_dotenv()
API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY not found in .env file. Please create one.")

# AI Model
MODEL_NAME = "gemini-2.5-flash"
API_URL = f"https://generativelanguage.googleapis.com/v1/models/{MODEL_NAME}:generateContent?key={API_KEY}"

# INit flask
app = Flask(__name__)
CORS(app)

@app.route('/api/summarize', methods=['POST'])
def summarize_pdf():
    if 'pdfFile' not in request.files:
        return jsonify({"error": "Brak pliku w żądaniu."}), 400

    file = request.files['pdfFile']
    
    
    file_content = file.read()
    
    
    is_valid, message = validate_pdf_file(file.filename, file_content)

    if not is_valid:
        return jsonify({"error": message}), 400

    try:
      
        pdf_reader = pypdf.PdfReader(io.BytesIO(file_content))
        
        extracted_text = ""
        for page in pdf_reader.pages:
            extracted_text += (page.extract_text() or "") + "\n"

        if not extracted_text.strip():
            return jsonify({"error": "Nie udało się wyodrębnić tekstu z pliku PDF."}), 400
    except Exception as e:
        return jsonify({"error": f"Nie można przetworzyć pliku PDF: {e}"}), 500
    
    try:
        print("Wysyłanie tekstu do modelu Gemini AI przez REST API...")
        
        prompt = f"""
        Jesteś ekspertem w analizie i streszczaniu dokumentów. Twoim zadaniem jest stworzenie zwięzłego podsumowania poniższego tekstu w języku polskim. 
        Podsumowanie powinno składać się z 3 do 5 kluczowych zdań, które oddają główną myśl dokumentu.

        Tekst do analizy:
        ---
        {extracted_text}
        ---
        """

        headers = {"Content-Type": "application/json"}
        data = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }

        response = requests.post(API_URL, headers=headers, json=data)
        response.raise_for_status()

        response_json = response.json()
        summary = response_json['candidates'][0]['content']['parts'][0]['text']
        
        print("Podsumowanie wygenerowane pomyślnie.")

    except requests.exceptions.RequestException as e:
        print(f"Błąd podczas komunikacji z API Gemini: {e}")
        if e.response is not None:
            print(f"Odpowiedź serwera: {e.response.text}")
        return jsonify({"error": "Wystąpił błąd podczas generowania podsumowania przez AI."}), 500
    except (KeyError, IndexError) as e:
        print(f"Nieoczekiwana struktura odpowiedzi od API Gemini: {e}")
        print(f"Otrzymana odpowiedź: {response_json}")
        return jsonify({"error": "Otrzymano nieprawidłową odpowiedź od serwera AI."}), 500

    return jsonify({
        "status": "success",
        "filename": file.filename,
        "summary": summary
    })

if __name__ == '__main__':
    app.run(debug=True)