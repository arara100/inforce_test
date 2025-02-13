from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count
from datetime import date
from api.models import Employee, Restaurant, Menu, Vote
from api.serializers import EmployeeSerializer, RestaurantSerializer, MenuSerializer, VoteSerializer, MenuBulkSerializer
from api.services.menu_service import bulk_upload_menus
from api.services.vote_service import create_vote, get_vote_results
from api.services.restaurant_service import create_restaurant

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.AllowAny]

class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['post'])
    def create_restaurant(self, request):
        name = request.data.get("name")
        restaurant = create_restaurant(name)
        return Response(RestaurantSerializer(restaurant).data)

class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def today(self, request):
        today_menu = Menu.objects.filter(date=date.today())
        serializer = self.get_serializer(today_menu, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def bulk_upload(self, request):
        serializer = MenuBulkSerializer(data=request.data)
        if serializer.is_valid():
            restaurant = serializer.validated_data['restaurant']
            menus_data = serializer.validated_data['menus']
            try:
                menus = bulk_upload_menus(restaurant, menus_data)
                return Response(MenuSerializer(menus, many=True).data, status=201)
            except ValueError as e:
                return Response({"error": str(e)}, status=400)
        return Response(serializer.errors, status=400)

class VoteViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        employee = request.user
        restaurant_id = request.data.get("restaurant")
        restaurant = Restaurant.objects.get(id=restaurant_id)
        try:
            vote = create_vote(employee, restaurant)
            return Response(VoteSerializer(vote).data)
        except ValueError as e:
            return Response({"error": str(e)}, status=400)

    @action(detail=False, methods=['get'])
    def results(self, request):
        results = get_vote_results()
        return Response(results)
