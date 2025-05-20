import PyPDF2
from transformers import pipeline
import torch

class PDFSummarizer:
    def __init__(self):
        # Using a lightweight summarization model
        self.summarizer = pipeline(
            "summarization",
            model="facebook/bart-large-cnn",
            device=0 if torch.cuda.is_available() else -1
        )
    
    def extract_text_from_pdf(self, pdf_file):
        """Extract text from PDF file"""
        text = ""
        try:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        except Exception as e:
            print(f"Error extracting text: {e}")
            return None
        return text
    
    def summarize_text(self, text, max_length=150):
        """Summarize the extracted text"""
        if not text or len(text.strip()) < 50:
            return "Text too short to summarize."
        
        try:
            # Split text into chunks if it's too long
            max_input_length = 1024
            if len(text) > max_input_length:
                # Take first chunk for simplicity
                text = text[:max_input_length]
            
            summary = self.summarizer(
                text,
                max_length=max_length,
                min_length=50,
                do_sample=False
            )
            return summary[0]['summary_text']
        except Exception as e:
            print(f"Error summarizing text: {e}")
            return "Error generating summary."
    
    def process_pdf(self, pdf_file):
        """Main method to process PDF and return summary"""
        text = self.extract_text_from_pdf(pdf_file)
        if not text:
            return "Could not extract text from PDF."
        
        summary = self.summarize_text(text)
        return summary