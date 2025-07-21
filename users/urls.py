# urls.py
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import TeamViewSet, UserViewSet

router = DefaultRouter()


router.register(r'user', UserViewSet)
router.register(r'team', TeamViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
