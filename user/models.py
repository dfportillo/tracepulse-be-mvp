from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    ROLE_TYPE = [
        ('operator', 'Operador'),
        ('supervisor', 'Supervisor'),
        ('admin', 'Administrador'),
        ('vendedor', 'Vendedor'),
        ('control', 'Control de calidad')
    ]
    role = models.CharField(max_length=50, choices=ROLE_TYPE,null=True, default='operator')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Teléfono')
    is_verified = models.BooleanField(default=False, verbose_name='Verificado')
    
    # Campos para tracking
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"