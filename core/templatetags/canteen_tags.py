from django import template
from core.models import Staff
from django.contrib.auth.models import AnonymousUser

register = template.Library()
@register.filter(name='is_staff_manager') 
def is_staff_manager(user):
    if not user.is_authenticated:
        return False
        
    return Staff.objects.filter(user=user, is_management=True).exists()

