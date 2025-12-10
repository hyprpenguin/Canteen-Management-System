from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Student(models.Model):
  user=models.OneToOneField(User, on_delete=models.CASCADE)

  student_id=models.CharField(max_length=10, unique=True)
  department=models.CharField(max_length=3,blank=True, null=True)
  mobile_number=models.CharField(max_length=14, blank=True, null=True)
  is_active = models.BooleanField(default=True)
  date_joined = models.DateTimeField(default=timezone.now)

  def __str__(self):
        return f"Student: {self.user.username} (Student ID: {self.student_id})"

class Faculty(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    faculty_id=models.CharField(max_length=10, unique=True)
    department=models.CharField(max_length=3,blank=True, null=True)
    mobile_number=models.CharField(max_length=14, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Faculty: {self.user.username} (Faculty ID: {self.faculty_id})"

    

class Staff(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)

    employee_id=models.CharField(max_length=6, unique=True)
    is_management = models.BooleanField(default=False)
    department=models.CharField(max_length=3, blank=True, null=True)
    mobile_number=models.CharField(max_length=14, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"Employee: {self.user.username} (Employee ID: {self.employee_id})"
    
class Category(models.Model):
    name=models.CharField(max_length=100, unique=True)
    description=models.TextField(blank=True, null=True, help_text="Description of food/drink category.")
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name'] 
        verbose_name_plural = "Categories"

class MenuItem(models.Model):
    name=models.CharField(max_length=50)

    category=models.ForeignKey(Category, on_delete=models.PROTECT)
    stock_quantity = models.IntegerField(default=0)
    description=models.TextField(blank=True, null=True)
    price=models.DecimalField(max_digits=5, decimal_places=2)
    is_available=models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.category.name})"
    
    class Meta:
        ordering = ['name']

class Order(models.Model):
    Status_choices= (
        ('accepted', 'Order Accepted (Awaiting Preparation)'),
        ('preparing', 'Preparing'),
        ('ready', 'Ready for Pickup'),
        ('pickedup', 'Picked Up(Completed)'),
        ('cancelled', 'Order Cancelled')
    )

    student=models.ForeignKey(
        'Student',
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )

    staff=models.ForeignKey(
        'Staff',
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )
    faculty = models.ForeignKey(
        'Faculty', 
        on_delete=models.PROTECT, 
        null=True, 
        blank=True
    )

    order_time=models.DateTimeField(
        auto_now_add=True,
        help_text="Time when order was created"
    )

    total_amount=models.DecimalField(
        max_digits=6,
        decimal_places=2
    )

    status=models.CharField(
        max_length=10,
        choices=Status_choices,
        default='accepted'
    )

    processed_by_staff = models.ForeignKey(
        'Staff', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='processed_orders',
        help_text="The staff member who finalized or marked the order as prepared."
    )

    def __str__(self):
        if self.student:
            return f"Order #{self.id} (Student: {self.student.user.username})"
        if self.faculty:
            return f"Order #{self.id} (Faculty: {self.faculty.user.username})"
        if self.staff:
            return f"Order #{self.id} (Staff: {self.staff.user.username})"
        return f"Order #{self.id} (Anonymous)"
    
    class Meta:
        ordering = ['-order_time']

class OrderDetails(models.Model):
    order=models.ForeignKey('Order', on_delete=models.CASCADE)
    item=models.ForeignKey('MenuItem', on_delete=models.CASCADE, help_text="The menu item purchased.")
    quantity=models.PositiveIntegerField(default=1)
    subtotal=models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.item.name} for Order #{self.order.id}"
    
    class Meta:
        verbose_name = "Order Detail"
        verbose_name_plural = "Order Details"
        