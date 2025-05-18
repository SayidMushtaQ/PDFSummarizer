import PyPDF2
from transformers import pipeline
from django.conf import settings
import os

class PDFSummarizer:
    def __init__(self):
        # Initialize the summarization pipeline
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    
    def extract_text_from_pdf(self, pdf_path):
        """Extract text from PDF file"""
        text = ""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text()
        except Exception as e:
            raise Exception(f"Error reading PDF: {str(e)}")
        return text
    
    def summarize_text(self, text, max_length=150, min_length=50):
        """Generate summary using BART model"""
        try:
            # Split text into chunks if it's too long (BART has input limits)
            max_chunk_length = 1024  # BART's max input length
            chunks = [text[i:i+max_chunk_length] for i in range(0, len(text), max_chunk_length)]
            
            summaries = []
            for chunk in chunks:
                if len(chunk.strip()) > 0:
                    summary = self.summarizer(chunk, 
                                            max_length=max_length, 
                                            min_length=min_length, 
                                            do_sample=False)
                    summaries.append(summary[0]['summary_text'])
            
            # Combine all summaries
            final_summary = ' '.join(summaries)
            
            # If we have multiple summaries, summarize them again
            if len(summaries) > 1:
                final_summary = self.summarizer(final_summary, 
                                               max_length=max_length, 
                                               min_length=min_length, 
                                               do_sample=False)[0]['summary_text']
            
            return final_summary
        except Exception as e:
            raise Exception(f"Error generating summary: {str(e)}")
    
    def process_pdf(self, pdf_path):
        """Complete PDF processing pipeline"""
        # Extract text
        text = self.extract_text_from_pdf(pdf_path)
        
        if not text.strip():
            raise Exception("No text could be extracted from the PDF")
        
        # Generate summary
        summary = self.summarize_text(text)
        
        return text, summary