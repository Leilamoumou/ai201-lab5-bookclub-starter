import pytest
from datetime import date, datetime, timedelta, timezone

from app import create_app, db
from models import Book, ReadingEvent, User
from services.reading_service import get_reading_history
from services.stats_service import calculate_streak


@pytest.fixture()
def app():
    app = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        }
    )
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


def test_calculate_streak_uses_finished_dates(app):
    today = date.today()
    base_time = datetime.now(timezone.utc).replace(hour=12, minute=0, second=0, microsecond=0)

    user = User(username="tester", email="tester@example.com", reading_streak=0)
    db.session.add(user)
    db.session.flush()

    books = [
        Book(title="Book 1", author="Author", pages=100, genre="fiction", added_by=user.id, added_at=base_time - timedelta(days=4)),
        Book(title="Book 2", author="Author", pages=120, genre="fiction", added_by=user.id, added_at=base_time - timedelta(days=3)),
        Book(title="Book 3", author="Author", pages=140, genre="fiction", added_by=user.id, added_at=base_time - timedelta(days=2)),
    ]
    db.session.add_all(books)
    db.session.flush()

    events = [
        ReadingEvent(
            user_id=user.id,
            book_id=books[0].id,
            started_at=base_time - timedelta(days=4),
            finished_at=base_time - timedelta(days=2),
        ),
        ReadingEvent(
            user_id=user.id,
            book_id=books[1].id,
            started_at=base_time - timedelta(days=3),
            finished_at=base_time - timedelta(days=1),
        ),
        ReadingEvent(
            user_id=user.id,
            book_id=books[2].id,
            started_at=base_time - timedelta(days=2),
            finished_at=base_time,
        ),
    ]
    db.session.add_all(events)
    db.session.commit()

    assert calculate_streak(user.id) == 3


def test_get_reading_history_orders_by_most_recently_finished(app):
    base_time = datetime.now(timezone.utc).replace(hour=12, minute=0, second=0, microsecond=0)

    user = User(username="reader", email="reader@example.com", reading_streak=0)
    db.session.add(user)
    db.session.flush()

    books = [
        Book(title="First Book", author="Author", pages=100, genre="fiction", added_by=user.id, added_at=base_time - timedelta(days=2)),
        Book(title="Second Book", author="Author", pages=120, genre="fiction", added_by=user.id, added_at=base_time - timedelta(days=1)),
    ]
    db.session.add_all(books)
    db.session.flush()

    events = [
        ReadingEvent(
            user_id=user.id,
            book_id=books[0].id,
            started_at=base_time - timedelta(days=2),
            finished_at=base_time - timedelta(days=1),
        ),
        ReadingEvent(
            user_id=user.id,
            book_id=books[1].id,
            started_at=base_time - timedelta(days=1),
            finished_at=base_time,
        ),
    ]
    db.session.add_all(events)
    db.session.commit()

    history = get_reading_history(user.id)

    assert [event.book.title for event in history] == ["Second Book", "First Book"]
