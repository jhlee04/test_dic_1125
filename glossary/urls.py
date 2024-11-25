from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # 용어 목록 페이지
    path('<int:pk>/', views.term_detail, name='term_detail'),  # 용어 상세 페이지
    path('upload/', views.upload_csv, name='upload_csv'),  # CSV 업로드 페이지
    path('<int:pk>/edit/', views.edit_term, name='edit_term'),  # 용어 수정 페이지
]
