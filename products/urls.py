from django.urls import path, include
from rest_framework import routers
from .views import ProductView, ComponentView, ProcessView, MachineView

router = routers.DefaultRouter()
router.register(r'products', ProductView, 'products')
router.register(r'components', ComponentView, 'components')
router.register(r'processes', ProcessView, 'processes')
router.register(r'machines', MachineView, 'machines')


urlpatterns = [
    path("api/", include(router.urls))
]
