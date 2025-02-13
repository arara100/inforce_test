from django.db.models import Count

from api.models import Vote, Restaurant
from datetime import date


def create_vote(employee, restaurant, vote_date=None):
    vote_date = vote_date or date.today()

    if Vote.objects.filter(employee=employee, date=vote_date).exists():
        raise ValueError("Ви вже проголосували сьогодні")

    vote = Vote.objects.create(employee=employee, restaurant=restaurant, date=vote_date)
    return vote


def get_vote_results(vote_date=None):
    vote_date = vote_date or date.today()
    today_votes = Vote.objects.filter(date=vote_date).values("restaurant").annotate(count=Count("restaurant"))
    results = {Restaurant.objects.get(id=v["restaurant"]).name: v["count"] for v in today_votes}
    return results
