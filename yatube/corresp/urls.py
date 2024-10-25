from django.urls import path

from . import views

urlpatterns = [
    path('', views.all_corresp, name='all_corresp'),
    path('sort/<int:cor_type_id>/<int:in_out_id>/', views.all_corresp_sort, name='all_corresp_sort'),
    path('new/<int:cor_type_id>/', views.corresp_new, name='corresp_new'),
    path('delete/<int:cor_id>/', views.corresp_delete, name='corresp_delete'),
    path('edit/<int:cor_id>/', views.corresp_edit, name='corresp_edit'),
    path('who_new/', views.who_new, name='who_new'),
] 
