from django.contrib import admin
from .models import PDFDocument

@admin.register(PDFDocument)
class PDFDocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'uploaded_at', 'has_summary']
    list_filter = ['uploaded_at']
    search_fields = ['title']
    readonly_fields = ['uploaded_at']
    ordering = ['-uploaded_at']
    
    def has_summary(self, obj):
        return bool(obj.summary)
    has_summary.boolean = True
    has_summary.short_description = 'Has Summary'
    
    fieldsets = (
        ('Document Information', {
            'fields': ('title', 'pdf_file', 'uploaded_at')
        }),
        ('Summary', {
            'fields': ('summary',),
            'classes': ('wide',),
        }),
    )