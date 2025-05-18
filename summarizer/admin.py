from django.contrib import admin
from .models import PDFDocument, Summary

@admin.register(PDFDocument)
class PDFDocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'uploaded_at']
    list_filter = ['uploaded_at']
    search_fields = ['title']
    readonly_fields = ['uploaded_at']

@admin.register(Summary)
class SummaryAdmin(admin.ModelAdmin):
    list_display = ['document', 'created_at']
    list_filter = ['created_at']
    readonly_fields = ['created_at']
    raw_id_fields = ['document']