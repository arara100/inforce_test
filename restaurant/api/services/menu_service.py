from django.db import IntegrityError
from datetime import date
from api.models import Menu


def bulk_upload_menus(restaurant, menus_data):
    menus = []
    for menu_data in menus_data:
        try:
            date_value = menu_data.get('date', date.today())
            menu, created = Menu.objects.get_or_create(
                restaurant=restaurant,
                date=date_value,
                defaults={'items': menu_data.get('items', '')}
            )
            menus.append(menu)
        except IntegrityError as e:
            raise ValueError(f"Помилка при створенні меню: {e}")
    return menus
