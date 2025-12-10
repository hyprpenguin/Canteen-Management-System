from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages 
from django.db import transaction 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from .models import Order, OrderDetails, MenuItem, Student, Staff, Faculty, Category
from django.views.generic.edit import DeleteView

def welcome_page(request):
    if request.GET.get('logout') == 'true':
        if request.user.is_authenticated:
            logout(request)
            messages.info(request, "You have been logged out successfully.")
        return redirect('welcome_page') 
        
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



def is_staff_manager(user): 
    if not user.is_authenticated:
        return False
    return Staff.objects.filter(user=user, is_management=True).exists()



@login_required
@user_passes_test(is_staff_manager) 
    

def is_staff_user(user):
    
    if user.is_authenticated:
        try:
            return Staff.objects.filter(user=user).exists()
        except Exception:
            return False
    return False

@login_required 
@user_passes_test(is_staff_manager) 


def staff_dashboard(request):
    pending_statuses = ['accepted', 'preparing', 'ready']
    pending_orders = Order.objects.filter(status__in=pending_statuses).order_by('order_time')
    
    username = request.user.username
    context = {
        'title': 'Canteen Management Dashboard',
        'pending_orders': pending_orders,
        'order_count': pending_orders.count(),
    }
    return render(request, 'core/staff_dashboard.html', context)


def order_detail_view(request, order_id):

    order=get_object_or_404(Order, id=order_id)
    order_details=OrderDetails.objects.filter(order=order)
    if request.method == 'POST':
        new_status = request.POST.get('status')

        if new_status:
            order.status = new_status
            order.save()
            messages.success(request, f"Order #{order.id} status updated to {new_status}!")
            return redirect('staff_dashboard') 
        else:
            messages.error(request, "Error: No status selected.")
            return redirect('order_detail', order_id=order_id)
        
    
    STATUS_CHOICES = ['PENDING', 'PREPARING', 'READY', 'COMPLETED', 'CANCELLED']
    context = {
        'order': order,
        'order_details': order_details,
        'status_choices': STATUS_CHOICES,
        'customer_type': order.get_customer_type(),
    }
    return render(request, 'core/order_detail.html', context)


@user_passes_test(is_staff_manager)
def manager_order_queue(request):
    active_orders = Order.objects.exclude(status__in=['pickedup', 'cancelled']).order_by('order_time')
    
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        new_status = request.POST.get('new_status')
        
        try:
            order = Order.objects.get(id=order_id)
            
            order.status = new_status
            
            order.save()
            
            messages.success(request, f"Order #{order_id} status updated to '{order.get_status_display()}'.")
        except Order.DoesNotExist:
            messages.error(request, "Order not found.")
        except Exception as e:
             messages.error(request, f"An error occurred: {e}")
             
        return redirect('manager_order_queue') 

    context = {
        'active_orders': active_orders,
        'status_choices': Order.Status_choices, 
    }
    return render(request, 'core/manager_order_queue.html', context)

      

def staff_login(request):
    role = "Staff/Manager"
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            try:
                staff_profile = Staff.objects.get(user=user)
                
                login(request, user)
                
                if staff_profile.is_management:
                    messages.success(request, f"Welcome, Canteen Manager {user.username}!")
                    return redirect('staff_dashboard')
                else:
                    messages.success(request, f"Welcome, Canteen Employee {user.username}!")
                    return redirect('menu_list') 
                    
            except Staff.DoesNotExist:
                messages.error(request, "Access denied. Your account is not linked to a Staff role.")
                
        else:
            messages.error(request, "Invalid username or password.")
            
    context = {'role': role}
    return render(request, 'core/login.html', context)



def employee_login(request):
    role = "Employee"
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            try:
                Staff.objects.get(user=user)
                login(request, user)
                
                return redirect('menu_list') 
                
            except Staff.DoesNotExist:
                messages.error(request, "Invalid credentials or account type mismatch.")
        else:
            messages.error(request, "Invalid username or password.")

    context = {'role': role}
    return render(request, 'core/login.html', context) 
            
  

     

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



@login_required
def place_order(request):
  customer = None
  customer_type = None

  try:
        customer = Student.objects.get(user=request.user)
        customer_type = 'student'
  except Student.DoesNotExist:
        try:
            customer = Faculty.objects.get(user=request.user)
            customer_type = 'faculty'
        except Faculty.DoesNotExist:
            try:
                customer = Staff.objects.get(user=request.user)
                customer_type = 'staff'
            except Staff.DoesNotExist:
                messages.error(request, "Error: User profile not linked to any account type.")
                return redirect('welcome_page')



  if request.method=='POST':
    with transaction.atomic():
            total_amount = 0
            line_items_to_save = []
            
            
            for key, quantity_str in request.POST.items():
                if key.startswith('item_') and quantity_str and int(quantity_str) > 0:
        
                    item_id = key.split('_')[1] 
                    quantity = int(quantity_str)
        
                    try:
                        menu_item = MenuItem.objects.select_for_update().get(id=item_id, is_available=True) 
                    except MenuItem.DoesNotExist:
                        messages.error(request, "Error: One of the selected items is unavailable.")
                        return redirect('place_order')
            
        
                    if menu_item.stock_quantity < quantity:
                        messages.error(request, f"Error: Only {menu_item.stock_quantity} of {menu_item.name} are in stock. Please reduce the quantity.")
                        return redirect('place_order') 

                    subtotal = menu_item.price * quantity
                    total_amount += subtotal
        
                    menu_item.stock_quantity -= quantity
                    menu_item.save() 
                    line_items_to_save.append({
                        'item': menu_item,
                        'quantity': quantity,
                        'subtotal': subtotal
        })

                
            if not line_items_to_save:
                messages.error(request, "Please select at least one item.")
                return redirect('place_order')    
            
            order_kwargs = {
                'total_amount': total_amount,
                customer_type: customer 
            }
            new_order = Order.objects.create(**order_kwargs)

            order_details = [
                OrderDetails(
                    order=new_order,
                    item=data['item'],
                    quantity=data['quantity'],
                    subtotal=data['subtotal']
                ) for data in line_items_to_save
            ]

            OrderDetails.objects.bulk_create(order_details)
            
            messages.success(request, f"Order #{new_order.id} placed successfully! Total: TK{total_amount:.2f}")
            return redirect('menu_list')
  else:
    categories = Category.objects.filter(is_active=True).order_by('name')
    menu_data = {}
    for category in categories:
        items = MenuItem.objects.filter(category=category, is_available=True, stock_quantity__gt=0).order_by('name')
        if items:
            menu_data[category] = items
        
    context = {
        'menu_data': menu_data,
        'customer_type': customer_type
    }
    return render(request, 'core/order_create.html', context)
  
class ManagerRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return is_staff_manager(self.request.user)

    def handle_no_permission(self):
        messages.error(self.request, "Access denied. Only Canteen Managers can access this page.")
        return redirect('welcome_page')
    
class MenuItemListView(ManagerRequiredMixin, ListView):
    model = MenuItem
    template_name = 'core/manager_menu_list.html' 
    context_object_name = 'menu_items'
    ordering = ['category', 'name']

class MenuItemCreateView(ManagerRequiredMixin, CreateView):
    model = MenuItem
    template_name = 'core/manager_menu_form.html'
    fields = ['category', 'name', 'description', 'price', 'stock_quantity', 'is_available']
    success_url = reverse_lazy('manager_menu_list') 

    def form_valid(self, form):
        messages.success(self.request, f"Menu item '{form.instance.name}' added successfully.")
        return super().form_valid(form)
    
class MenuItemUpdateView(ManagerRequiredMixin, UpdateView):
    model = MenuItem
    template_name = 'core/manager_menu_form.html' 
    fields = ['category', 'name', 'description', 'price', 'stock_quantity', 'is_available']
    success_url = reverse_lazy('manager_menu_list')

    def form_valid(self, form):
        messages.success(self.request, f"Menu item '{form.instance.name}' updated successfully.")
        return super().form_valid(form)
    
class MenuItemDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = MenuItem
    template_name = 'core/menu_item_confirm_delete.html'
    
    success_url = reverse_lazy('manager_menu_list') 

    def test_func(self):
        return is_staff_manager(self.request.user)
    
    def form_valid(self, form):
        messages.success(self.request, f"Menu item '{self.object.name}' has been successfully deleted.")
        return super().form_valid(form)
    
class CategoryCreateView(ManagerRequiredMixin, CreateView):
    model = Category
    template_name = 'core/manager_category_form.html'
    fields = ['name']
    success_url = reverse_lazy('manager_menu_list') 

    def form_valid(self, form):
        messages.success(self.request, f"Category '{form.instance.name}' added successfully.")
        return super().form_valid(form)





        messages.success(request, "Your order has been successfully placed!")
        return redirect('menu_list')

  


