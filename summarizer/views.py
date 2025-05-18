from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import PDFDocument, Summary
from .forms import PDFUploadForm
from .utils import PDFSummarizer


def upload_pdf(request):
    """Handle PDF upload and processing"""
    if request.method == 'POST':
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the uploaded PDF
            document = form.save()
            
            try:
                # Initialize summarizer
                summarizer = PDFSummarizer()
                
                # Process the PDF
                pdf_path = document.pdf_file.path
                original_text, summary_text = summarizer.process_pdf(pdf_path)
                
                # Save the summary
                Summary.objects.create(
                    document=document,
                    original_text=original_text,
                    summary_text=summary_text
                )
                
                messages.success(request, 'PDF uploaded and summarized successfully!')
                return redirect('summary_detail', document_id=document.id)
                
            except Exception as e:
                messages.error(request, f'Error processing PDF: {str(e)}')
                document.delete()  # Remove the document if processing fails
    else:
        form = PDFUploadForm()
    
    return render(request, 'summarizer/upload.html', {'form': form})

def summary_detail(request, document_id):
    """Display summary details"""
    document = get_object_or_404(PDFDocument, id=document_id)
    try:
        summary = Summary.objects.get(document=document)
    except Summary.DoesNotExist:
        messages.error(request, 'Summary not found.')
        return redirect('upload_pdf')
    
    context = {
        'document': document,
        'summary': summary,
    }
    return render(request, 'summarizer/summary_detail.html', context)

def document_list(request):
    """List all processed documents"""
    documents = PDFDocument.objects.all().order_by('-uploaded_at')
    return render(request, 'summarizer/document_list.html', {'documents': documents})

def home(request):
    """Home page"""
    return render(request, 'summarizer/home.html')