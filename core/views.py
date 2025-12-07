from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages 
from django.db import transaction 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Order, OrderDetails, MenuItem, Student, Staff, Faculty, Category

def welcome_page(request):
    """Displays the welcome page with buttons to select the account type."""
    return render(request, 'core/welcome.html')

def student_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            try:
                Student.objects.get(user=user)
                login(request, user) 
                messages.success(request, f"Welcome, Student {user.username}!")
                return redirect('menu_list')
            except Student.DoesNotExist:
                messages.error(request, "Invalid credentials or account type mismatch.")
        else:
            messages.error(request, "Invalid username or password.")
        
    return render(request, 'core/login.html', {'role': 'Student'})

def faculty_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            try:
                Faculty.objects.get(user=user)
                login(request, user)
                messages.success(request, f"Welcome, Faculty {user.username}!")
                return redirect('menu_list')
            except Faculty.DoesNotExist:
                messages.error(request, "Invalid credentials or account type mismatch.")
        else:
            messages.error(request, "Invalid username or password.")
            
    return render(request, 'core/login.html', {'role': 'Faculty'})

def is_staff_user(user):
    
    if user.is_authenticated:
        try:
            return Staff.objects.filter(user=user).exists()
        except Exception:
            return False
    return False

@login_required 
@user_passes_test(is_staff_user) 


def staff_dashboard(request):
    
    
    context = {
        'title': 'Canteen Management Dashboard',
    }
    return render(request, 'core/staff_dashboard.html', context)
      

def staff_login(request):
    # This block is for handling the form SUBMISSION
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            try:
                Staff.objects.get(user=user)
                login(request, user)
                messages.success(request, f"Welcome, Staff {user.username}!")
                return redirect('staff_dashboard')
            except Staff.DoesNotExist:
                messages.error(request, "Invalid credentials or account type mismatch.") 
        else:
            messages.error(request, "Invalid username or password.")
            
    
    return render(request, 'core/login.html', {'role': 'Staff'})
            
  

     

def menu_list(request):
  categories=Category.objects.filter(is_active=True).order_by('name')
  menu_data={}

  for category in categories:
    items=MenuItem.objects.filter(category=category, is_available=True).order_by('name')

    if items:
      menu_data[category]=items

      
      
  context={
      'menu_data': menu_data
      }

  return render(request, 'core/menu_list.html',context)




def place_order(request):

  if request.method=='POST':




    messages.success(request, "Your order has been successfully placed!")
    return redirect('menu_list')

  

# Create your views here.
