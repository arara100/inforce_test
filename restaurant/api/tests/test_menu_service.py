from django.test import TestCase
from api.models import Restaurant, Menu
from api.services.menu_service import bulk_upload_menus
from datetime import date


class MenuServiceTest(TestCase):
    def setUp(self):
        self.restaurant = Restaurant.objects.create(name="Test Restaurant")

    def test_bulk_upload_menus(self):
        menus_data = [
            {"date": str(date.today()), "items": "Піца, Суп, Салат"},
            {"date": "2025-02-15", "items": "Паста, Лазанья"},
        ]
        menus = bulk_upload_menus(self.restaurant, menus_data)

        self.assertEqual(len(menus), 2)
        self.assertTrue(Menu.objects.filter(restaurant=self.restaurant, date=date.today()).exists())
        self.assertTrue(Menu.objects.filter(restaurant=self.restaurant, date="2025-02-15").exists())

    def test_bulk_upload_menus_duplicate(self):
        """Тестуємо, що при повторному завантаженні меню на той самий день не створюється дубль."""
        menus_data = [{"date": str(date.today()), "items": "Піца, Суп, Салат"}]
        bulk_upload_menus(self.restaurant, menus_data)
        bulk_upload_menus(self.restaurant, menus_data)

        self.assertEqual(Menu.objects.filter(date=date.today()).count(), 1)
