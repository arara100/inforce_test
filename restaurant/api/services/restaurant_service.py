from api.models import Restaurant


def create_restaurant(name):
    restaurant, created = Restaurant.objects.get_or_create(name=name)
    return restaurant
