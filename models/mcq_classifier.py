import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer
import sqlite3

# Load the pre-trained T5 model for classification
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model_name = 'google/flan-t5-small'
model = T5ForConditionalGeneration.from_pretrained(model_name).to(device)
tokenizer = T5Tokenizer.from_pretrained(model_name)

# Dummy Bloom levels classifier (simple prompt-based method)
def classify_bloom_level(mcq_text):
    prompt = f"Classify the Bloom level for this MCQ: '{mcq_text}'"
    input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to(device)
    with torch.no_grad():
        output = model.generate(input_ids, max_length=10, num_beams=5)
    bloom_level = tokenizer.decode(output[0], skip_special_tokens=True)
    return bloom_level.strip().lower()

# Function to classify and store MCQs in the database
def classify_and_store_mcqs():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    
    # Fetch all MCQs from the database
    c.execute('SELECT id, question FROM mcqs')
    mcqs = c.fetchall()
    
    for mcq_id, mcq_text in mcqs:
        # Classify Bloom level
        bloom_level = classify_bloom_level(mcq_text)
        
        # Update MCQs with Bloom level
        c.execute('''
            UPDATE mcqs
            SET bloom_level = ?
            WHERE id = ?
        ''', (bloom_level, mcq_id))
    
    conn.commit()
    conn.close()
    print("MCQs classified with Bloom levels.")

if __name__ == "__main__":
    classify_and_store_mcqs()
