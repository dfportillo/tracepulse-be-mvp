from django.db import models
from user.models import User

class Machine(models.Model):
    MACHINE_CHOICES = [
        ('lathe', 'Torno'),
        ('milling', 'Fresado'),
        ('welding', 'Soldadora'),
        ('painting', 'Pintura'),
        ('packing', 'Embalaje'),
        ('assembly', 'Montaje')
    ]
    STATE_CHOICES = [
        ('free', 'Libre'),
        ('busy', 'Ocupada'),
        ('in_preparation', 'En preparación')
    ]
    name = models.CharField(max_length=40, verbose_name='Nombre maquina')
    machine_type = models.CharField(
        max_length=50,
        choices=MACHINE_CHOICES,
        default='lathe',
        verbose_name='Tipo de maquina'
    )
    state = models.CharField(
        max_length=50,
        choices=STATE_CHOICES,
        default='free',
        verbose_name='Estado actual'
    )

    class Meta:
        verbose_name = "Maquina"
        verbose_name_plural = "Maquinas"
        ordering = ['machine_type']

    def __str__(self):
        return f"{self.name}"

class Process(models.Model):
    PROCESS_TYPE_CHOICES = [
        ('cutting', 'Corte'),
        ('welding', 'Soldadura'),
        ('assembly', 'Ensamblaje'),
        ('painting', 'Pintura'),
        ('testing', 'Pruebas'),
    ]
    PROCESS_SOURCE_CHOICES = [
        ('internal', 'Interno'),
        ('external', 'Externalizado'),
    ]

    name = models.CharField(max_length=100, default="Proceso", verbose_name="Nombre del proceso")
    process_type = models.CharField(
        max_length=40,
        choices=PROCESS_TYPE_CHOICES,
        default='assembly',
        verbose_name='Tipo de proceso'
    )
    process_source = models.CharField(
        max_length=20,
        choices=PROCESS_SOURCE_CHOICES,
        default='internal',
        verbose_name="Origen del proceso"
    )
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    machines = models.ManyToManyField(Machine, verbose_name="Maquinas")

    class Meta:
        verbose_name = "Proceso"
        verbose_name_plural = "Procesos"
        ordering = ['process_type']

    def __str__(self):
        return f"{self.name} - {self.process_type}"

class Component(models.Model):
    TYPE_CHOICES = [
        ('fabricated', 'Fabricado'),
        ('purchased', 'Comprado'),
    ]

    name = models.CharField(max_length=100, verbose_name="Nombre del componente")
    comp_id = models.CharField(max_length=100, unique=True, verbose_name="Código")
    description = models.TextField(blank=True, verbose_name="Descripción")
    component_type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        default='purchased',
        verbose_name="Tipo de componente"
    )
    manufacturing_process = models.ManyToManyField(Process, verbose_name="Proceso de manufactura")

    class Meta:
        verbose_name = "Componente"
        verbose_name_plural = "Componentes"
        ordering = ['name']

    def __str__(self):
        return f"{self.comp_id} - {self.name}"

class Product(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Baja'),
        ('medium', 'Media'),
        ('high', 'Alta'),
    ]

    STATUS_CHOICES = [
        (0, 'No iniciado'),
        (25, '25% Completado'),
        (50, '50% Completado'),
        (75, '75% Completado'),
        (100, '100% Completado'),
    ]

    op_value = models.CharField(max_length=100, verbose_name="Orden de Producción")
    name = models.CharField(max_length=100, verbose_name="Nombre producto")
    description = models.TextField(blank=True, verbose_name="Descripción")
    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default='medium',
        verbose_name="Prioridad"
    )
    status = models.IntegerField(
        choices=STATUS_CHOICES,
        default=0,
        verbose_name="Estado de producción"
    )
    components = models.ManyToManyField(Component, verbose_name="Componentes")
    quantity = models.IntegerField(default=0, verbose_name="Cantidad de productos a fabricar")
    start_date = models.DateField(auto_now_add=True, verbose_name="Fecha de inicio")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última actualización")
    end_date = models.DateField(null=True, blank=True, verbose_name="Fecha de finalización")
    notes = models.TextField(blank=True, verbose_name="Notas adicionales")

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['-priority', 'op_value']

    def __str__(self):
        return self.op_value

    @property
    def progress(self):
        return f"{self.status}%"
