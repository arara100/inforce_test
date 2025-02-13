from rest_framework import serializers
from .models import Employee, Restaurant, Menu, Vote
from datetime import date


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'username', 'email', 'department', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = Employee.objects.create_user(**validated_data)
        return user


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'


class MenuBulkSerializer(serializers.Serializer):
    restaurant = serializers.PrimaryKeyRelatedField(queryset=Restaurant.objects.all())
    menus = serializers.ListField(
        child=serializers.DictField(
            child=serializers.CharField(max_length=255)
        )
    )

    def create(self, validated_data):
        restaurant = validated_data['restaurant']
        menus_data = validated_data['menus']

        menus = []
        for menu_data in menus_data:
            date_value = menu_data.get('date', date.today())
            menu, created = Menu.objects.get_or_create(
                restaurant=restaurant,
                date=date_value,
                defaults={'items': menu_data.get('items', '')}
            )
            menus.append(menu)
        return menus


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = '__all__'
