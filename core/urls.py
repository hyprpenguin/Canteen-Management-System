from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome_page, name='welcome_page'),
    path('login/student/', views.student_login, name='student_login'),
    path('login/faculty/', views.faculty_login, name='faculty_login'),
    path('login/staff/', views.staff_login, name='staff_login'),
    path('management/dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('menu/', views.menu_list, name='menu_list'),
    path('order/new/', views.place_order, name='place_order'),
]