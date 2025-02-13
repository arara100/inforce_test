from django.test import TestCase
from api.models import Employee, Restaurant, Vote
from api.services.vote_service import create_vote, get_vote_results
from datetime import date


class VoteServiceTest(TestCase):
    def setUp(self):
        self.employee = Employee.objects.create_user(username="testuser", password="password")
        self.restaurant = Restaurant.objects.create(name="Test Restaurant")

    def test_create_vote(self):
        vote = create_vote(self.employee, self.restaurant)
        self.assertEqual(Vote.objects.count(), 1)
        self.assertEqual(vote.employee, self.employee)
        self.assertEqual(vote.restaurant, self.restaurant)

    def test_create_vote_twice(self):
        """Користувач не може проголосувати двічі в один день."""
        create_vote(self.employee, self.restaurant)
        with self.assertRaises(ValueError):
            create_vote(self.employee, self.restaurant)

    def test_get_vote_results(self):
        """Перевіряємо підрахунок голосів."""
        create_vote(self.employee, self.restaurant)
        results = get_vote_results()
        self.assertEqual(results[self.restaurant.name], 1)
