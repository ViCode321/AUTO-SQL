#app/urls.py
from django.urls import path, include

from app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='home'),
    path('insert/', views.insert_view, name='insert'),
    path('delete/', views.delete_view, name='delete'),
    path('submit_excel/', views.submit_excel, name='submit_excel'),
    path('submit_excel_sql/', views.submit_excel_sql, name='submit_excel_sql'),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
