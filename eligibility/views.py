from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
import os
import json
import openai
from sentence_transformers import SentenceTransformer, util
import pytesseract
from PIL import Image
import cv2
import numpy as np
import pytesseract

# Explicitly set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"



# ✅ Load your OpenAI API key (DO NOT hardcode in production)
openai.api_key = "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"

# ✅ Load CSV and sentence embeddings once
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(BASE_DIR, 'eligibility', 'data', 'schemes.csv')

df = pd.read_csv(CSV_PATH)
df.rename(columns={"apply": "link"}, inplace=True)

combined_text = (df["description"] + ". " + df["eligibility"]).tolist()

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
embeddings = model.encode(combined_text, convert_to_tensor=True)

# ✅ Views

def landing_page(request):
    return render(request, 'eligibility/landing.html')

def eligibility_form(request):
    return render(request, 'eligibility/form.html')

def submit(request):
    if request.method == "POST":
        name = request.POST.get("name")
        age = request.POST.get("age")
        income = request.POST.get("income")
        caste = request.POST.get("caste")
        state = request.POST.get("state")

        user_description = f"{name}, {age} years old, from {state}, caste: {caste}, income: ₹{income}"
        input_embedding = model.encode(user_description, convert_to_tensor=True)
        scores = util.pytorch_cos_sim(input_embedding, embeddings)[0]
        top_indices = scores.argsort(descending=True)[:3]

        top_schemes = []
        for idx in top_indices:
            idx = idx.item()
            top_schemes.append({
                'name': df.iloc[idx]['name'],
                'description': df.iloc[idx]['description'],
                'eligibility': df.iloc[idx]['eligibility'],
                'documents': df.iloc[idx]['documents'],
                'apply': df.iloc[idx]['link']
            })

        return render(request, 'eligibility/result.html', {
            'name': name,
            'schemes': top_schemes,
            'input_description': user_description
        })

    return render(request, 'eligibility/form.html')

# ✅ JavaScript-based chatbot API endpoint
@csrf_exempt
def chatbot_ask(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_input = data.get("message", "")

            # Call OpenAI Chat API
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant for Indian government schemes."},
                    {"role": "user", "content": user_input}
                ]
            )

            reply = response.choices[0].message["content"]
            return JsonResponse({"response": reply})

        except Exception as e:
            return JsonResponse({"response": f"Error: {str(e)}"})

    return JsonResponse({"response": "Invalid request method."})
def chatbot_page(request):
    reply = None
    if request.method == "POST":
        question = request.POST.get("question")
        reply = ask_chatbot(question)

    return render(request, 'eligibility/chat.html', {
        'reply': reply
    })
from django.core.files.storage import FileSystemStorage

def upload_document(request):
    if request.method == 'POST' and request.FILES.get('document'):
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)
        file_path = fs.path(filename)

        # Load and process image
        image = cv2.imread(file_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        text = pytesseract.image_to_string(gray)

        # Sample keyword-based eligibility logic
        keywords = ['income', 'caste', 'residence', 'id', 'aadhaar']
        matched = sum(1 for kw in keywords if kw in text.lower())
        total = len(keywords)
        score = int((matched / total) * 100)

        missing = [kw for kw in keywords if kw not in text.lower()]
        
        return render(request, 'eligibility/analysis.html', {
            'score': score,
            'missing': missing,
            'text': text
        })

    return render(request, 'eligibility/upload.html')
