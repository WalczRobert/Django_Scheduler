from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib import admin
from core import views
urlpatterns = [
    path('', views.ScheduleCreate.as_view(), name="schedule_create"),
    path('accounts/login/',
         auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('accounts/logout/',
         auth_views.LogoutView.as_view(template_name='core/logout.html'), name='logout'),
    path('list/', views.ScheduleList.as_view(), name="schedule_list"),
    path('download/', views.export_csv, name="export_csv"),
    path('delete/<int:pk>/', views.ScheduleDelete.as_view(), name="schedule_delete"),
    path('admin/', views.admin_view, name="admin"),
]
