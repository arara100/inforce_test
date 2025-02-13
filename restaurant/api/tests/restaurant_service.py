from django.test import TestCase
from api.models import Restaurant
from api.services.restaurant_service import create_restaurant


class RestaurantServiceTest(TestCase):
    def test_create_restaurant(self):
        restaurant = create_restaurant("New Restaurant")
        self.assertEqual(Restaurant.objects.count(), 1)
        self.assertEqual(restaurant.name, "New Restaurant")

    def test_create_duplicate_restaurant(self):
        """Переконуємось, що дублікати ресторанів не створюються."""
        create_restaurant("New Restaurant")
        create_restaurant("New Restaurant")
        self.assertEqual(Restaurant.objects.count(), 1)
