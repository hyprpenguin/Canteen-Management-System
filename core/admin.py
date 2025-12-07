from django.contrib import admin
from .models import Student, Faculty, Staff, Category, MenuItem, Order, OrderDetails

# Register your models here.

admin.site.register(Student)
admin.site.register(Faculty)
admin.site.register(Staff)

admin.site.register(Category)
admin.site.register(MenuItem)

admin.site.register(Order)
admin.site.register(OrderDetails)

