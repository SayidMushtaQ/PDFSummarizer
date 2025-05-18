from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.upload_pdf, name='upload_pdf'),
    path('summary/<int:document_id>/', views.summary_detail, name='summary_detail'),
    path('documents/', views.document_list, name='document_list'),
]