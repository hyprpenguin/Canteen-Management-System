from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome_page, name='welcome_page'),
    path('menu/', views.menu_list, name='menu_list'),
    path('order/place/', views.place_order, name='place_order'),
    path('login/student/', views.student_login, name='student_login'),
    path('login/faculty/', views.faculty_login, name='faculty_login'),
    path('login/manager/', views.staff_login, name='canteen_manager_login'),
    path('login/employee/', views.employee_login, name='employee_login'),   
    path('management/dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('management/order/<int:order_id>/', views.order_detail_view, name='order_detail'),
    path('management/menu/list/', views.MenuItemListView.as_view(), name='manager_menu_list'),
    path('management/menu/add/', views.MenuItemCreateView.as_view(), name='manager_menu_add'),
    path('management/menu/edit/<int:pk>/', views.MenuItemUpdateView.as_view(), name='manager_menu_edit'),
    path('management/category/add/', views.CategoryCreateView.as_view(), name='manager_category_add'),
    path('management/menu/<int:pk>/delete/', views.MenuItemDeleteView.as_view(), name='menu_item_delete'),
    path('management/orders/queue/', views.manager_order_queue, name='manager_order_queue'),
]