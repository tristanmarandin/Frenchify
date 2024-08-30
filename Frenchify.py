## IMPORTS

import os
import pdfplumber
# from docx import Document
import requests
import json
# import win32com.client as win32


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

def extract_text_from_doc(doc_path):
    # Initialize the Word application
    word = win32.Dispatch("Word.Application")
    word.Visible = False  # Keep Word invisible during operation

    # Open the document
    doc = word.Documents.Open(doc_path)

    # Extract text from the document
    text = doc.Range().Text

    # Close the document and Word application
    doc.Close(False)
    word.Quit()

    return text
    

def chunk_text(text, max_length):
    chunks = []
    while len(text) > max_length:
        # Find the last space within the limit to avoid breaking words
        split_index = text.rfind(' ', 0, max_length)
        if split_index == -1:  # No space found, split at max_length
            split_index = max_length
        chunks.append(text[:split_index])
        text = text[split_index:].strip()
    chunks.append(text)  # Add remaining text
    return chunks


def translate_chunked(text):
    max_length = 10000
    chunks = chunk_text(text, max_length)
    translations = []
    
    for chunk in chunks:
        translation = translate(chunk)  # Existing translate function
        translations.append(translation)
    
    # Combine translations back into a single text
    full_translation = " ".join(translations)
    return full_translation


def translate(text):

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

    if response.status_code == 200:
        response_payload = response.json()
        body = json.loads(response_payload['body'])
        print("body: ", body)   
        generated_text_sequence = body['model_response']
        generated_text = "\n".join(generated_text_sequence.split("\n")[1:])
        print("generated_text: ", generated_text_sequence)
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
    elif file_path.endswith('.doc'):
        text = extract_text_from_doc(file_path)
    else:
        raise ValueError("Unsupported file format. Please provide a PDF or DOCX file.")
    print("Text extracted")

    translation = translate_chunked(text)
    print("Translation achieved")
    save_translation(translation, output_dir)
    print("Translation saved")

# Example usage
file_path = "C:/PythonProjects/Frenchify/englishTest.pdf"  
output_dir = "C:/PythonProjects/Frenchify/output_requirements"
language = "english"
main(file_path, output_dir)
