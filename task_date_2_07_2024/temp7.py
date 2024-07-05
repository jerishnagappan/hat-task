import os
import pandas as pd
import pdfplumber
from collections import Counter


def extract_pdf_resume(file_path):
    try:
        
        with pdfplumber.open(file_path) as pdf:
            
            resume_text = ''
            word_count = 0
            
            
            for page in pdf.pages:
                resume_text += page.extract_text()
                word_count += len(page.extract_words())

        
        word_counts = Counter(resume_text.split())
        most_common_word = word_counts.most_common(1)[0][0] if word_counts else ''
        
        
        resume_data = {
            'file_name': os.path.basename(file_path),
            'resume_text': resume_text,
            'word_count': word_count,
            'most_common_word': most_common_word
        }
        
        return resume_data
    
    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")
        return None


file_path = '/home/jovyan/work/resumes/Student Athlete Resume.pdf'
resume_data = extract_pdf_resume(file_path)

if resume_data:
    df = pd.DataFrame([resume_data])
    print(df)
else:
    print("Failed to read PDF resume.")
