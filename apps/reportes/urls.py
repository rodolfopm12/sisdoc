from django.urls import path

from apps.reportes.views import InvoicePDFView, Index
from . import views

urlpatterns = [
	path('', Index.as_view(), name="reportes"),
    # path('pdf_view/', views.ViewPDF.as_view(), name="pdf_view"),
    # path('pdf_download/', views.DownloadPDF.as_view(), name="pdf_download"),
    # path('reporte_pdf/<int:pk>/', InvoicePDFView.as_view(), name="reporte_pdf"),
    path('reporte_pdf/', InvoicePDFView.as_view(), name="reporte_general"),
]