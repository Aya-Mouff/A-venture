from django.urls import path
from pages.views.old_views import analyze_activity
from . import views

urlpatterns = [ 
    path('', views.login, name='home'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('admindashboard/', views.admindashboard, name='admin_dashboard'),
    path('delete_record/<int:record_id>/', views.delete_record, name='delete_record'),
    path('recordsmanagement/', views.records_management, name='recordsmanagement'),
    path('change_status/<int:record_id>/', views.change_status, name='change_status'),
    path("analyze/", analyze_activity, name="analyze_activity"),
    path('upload/', views.upload_file, name='upload_file'),

] 