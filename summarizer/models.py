from django.db import models

class PDFDocument(models.Model):
    title = models.CharField(max_length=255)
    pdf_file = models.FileField(upload_to='pdfs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class Summary(models.Model):
    document = models.OneToOneField(PDFDocument, on_delete=models.CASCADE)
    original_text = models.TextField()
    summary_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Summary for {self.document.title}"