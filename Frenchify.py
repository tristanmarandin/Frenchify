## IMPORTS

import os
import pdfplumber
from docx import Document
import requests
import json


## METHODS 

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text

def extract_text_from_word(docx_path):
    doc = Document(docx_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text
    
def translate(text):
    print("text: ", text)

    if language == "english":
        prompt = "Ta tâche est de traduire ce texte en français :" + text
    elif language == "french":
        prompt = "Your task is now to translate this text in english :" + text
    
    url = 'https://obxy6jphzf.execute-api.eu-west-1.amazonaws.com/dev/question'  
    payload = {
        'body': {
            'request': prompt.encode('utf-8').decode('latin-1')
        }
    }
    
    headers = {
        'Content-Type': 'application/json; charset=utf-8'
    }
    
    response = requests.post(url, json=payload, headers=headers)
    print("Response: ", response)

    if response.status_code == 200:
        response_payload = response.json()
        body = json.loads(response_payload['body'])
        print("body: ", body)   
        generated_text = body['model_response']
        print("generated_text: ", generated_text)
        return generated_text
    else:
        raise Exception(f"Request failed with status code {response.status_code}: {response.text}")


def save_translation(translation, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, f"translation.txt"), "w", encoding="utf-8") as file:
        file.write(translation)
            

## MAIN

def main(file_path, output_dir):
    if file_path.endswith('.pdf'):
        text = extract_text_from_pdf(file_path)
    elif file_path.endswith('.docx'):
        text = extract_text_from_word(file_path)
    else:
        raise ValueError("Unsupported file format. Please provide a PDF or DOCX file.")
    print("Text extracted")

    translation = translate(text)
    print("Translation achieved")
    save_translation(translation, output_dir)
    print("Translation saved")

# Example usage
file_path = "C:/PythonProjects/Frenchify/englishTest.pdf"  # Change to your file path
output_dir = "C:/PythonProjects/Frenchify/output_requirements"
language = "english"
main(file_path, output_dir)
