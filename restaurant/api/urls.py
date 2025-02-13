from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import EmployeeViewSet, RestaurantViewSet, MenuViewSet, VoteViewSet

router = DefaultRouter()
router.register(r'employees', EmployeeViewSet, basename='employee')
router.register(r'restaurants', RestaurantViewSet, basename='restaurant')
router.register(r'menus', MenuViewSet, basename='menu')
router.register(r'votes', VoteViewSet, basename='vote')

urlpatterns = [
    path('', include(router.urls)),
]
