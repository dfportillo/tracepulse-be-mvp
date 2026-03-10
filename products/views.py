from rest_framework import viewsets
from .serializer import ProductSerializer, ComponentSerializer, ProcessSerializer, MachineSerializer
from .models import Product, Component, Process, Machine
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.middleware.csrf import get_token

# Create your views here.
class MachineView(viewsets.ModelViewSet):
    serializer_class = MachineSerializer
    queryset = Machine.objects.all()

class ProcessView(viewsets.ModelViewSet):
    serializer_class = ProcessSerializer
    queryset = Process.objects.all()

class ComponentView(viewsets.ModelViewSet):
    serializer_class = ComponentSerializer
    queryset = Component.objects.all()

class ProductView(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()