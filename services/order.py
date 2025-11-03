from datetime import datetime

from django.db import transaction
from django.db.models import QuerySet

from db.models import Ticket, Order, User, MovieSession


def create_order(
        tickets: list[dict],
        username: str,
        date: datetime = None
) -> None:
    with transaction.atomic():
        user = User.objects.get(username=username)

        if not user:
            raise Exception("User not found")

        order = Order.objects.create(user=user)

        if date:
            order.created_at = date
            order.save()

        sessions = MovieSession.objects.all()
        print(sessions)

        for ticket in tickets:
            session = sessions.get(id=ticket["movie_session"])

            if not session:
                raise Exception("Session not found")

            Ticket.objects.create(
                order=order,
                row=ticket["row"],
                seat=ticket["seat"],
                movie_session=session
            )


def get_orders(username: str = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
