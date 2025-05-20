from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import PDFUploadForm
from .models import PDFDocument
from .utils import PDFSummarizer

def upload_pdf(request):
    if request.method == 'POST':
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the form but don't commit to database yet
            pdf_document = form.save(commit=False)
            
            # Process the PDF and generate summary
            summarizer = PDFSummarizer()
            summary = summarizer.process_pdf(pdf_document.pdf_file)
            pdf_document.summary = summary
            
            # Now save to database
            pdf_document.save()
            
            messages.success(request, 'PDF uploaded and summarized successfully!')
            return redirect('view_summary', pk=pdf_document.pk)
    else:
        form = PDFUploadForm()
    
    return render(request, 'summarizer/upload.html', {'form': form})

def view_summary(request, pk):
    pdf_document = get_object_or_404(PDFDocument, pk=pk)
    return render(request, 'summarizer/summary.html', {'document': pdf_document})

def document_list(request):
    documents = PDFDocument.objects.all().order_by('-uploaded_at')
    return render(request, 'summarizer/list.html', {'documents': documents})