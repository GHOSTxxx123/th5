from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ResourceViewSet, BookingViewSet

router = DefaultRouter()
router.register(r'resource', ResourceViewSet)
router.register(r'booking', BookingViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
