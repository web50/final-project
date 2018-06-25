from django.contrib import admin

# Register your models here.

from .models import Portfolio, Customer

admin.site.register(Portfolio)
admin.site.register(Customer)
