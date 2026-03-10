from django.contrib import admin
from .models import Product, Component, Process, Machine

# Register your models here.
admin.site.register(Product)
admin.site.register(Component)
admin.site.register(Process)
admin.site.register(Machine)
