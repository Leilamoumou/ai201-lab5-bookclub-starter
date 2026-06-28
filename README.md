# BookClub — AI201 Lab 5 Starter

A small reading list app where club members track books, log their progress, and see their reading stats.

## What the app does

- **Book list** — members add books to a shared reading list
- **Reading tracker** — mark books as started or finished
- **Stats** — reading streak, books finished this month, total pages read

## Setup

```bash
python -m venv .venv
source .venv/bin/activate      # Mac/Linux
# or: .venv\Scripts\activate   # Windows

pip install -r requirements.txt

python seed_data.py    # populate the database
python app.py          # start the server (runs at http://127.0.0.1:5000)
```

## API

| Method | Endpoint                        | Description                          |
|--------|---------------------------------|--------------------------------------|
| GET    | `/books/`                       | List all books                       |
| POST   | `/books/`                       | Add a book                           |
| POST   | `/reading/start`                | Mark a book as started               |
| POST   | `/reading/finish`               | Mark a book as finished              |
| GET    | `/reading/current/<user_id>`    | Books a user is currently reading    |
| GET    | `/reading/history/<user_id>`    | Books a user has finished            |
| GET    | `/stats/<user_id>`              | Reading streak, books this month, total pages |

## Codebase structure

```plaintext
app.py                  Flask application factory
models.py               SQLAlchemy models: User, Book, ReadingEvent
routes/
  books.py              Book list endpoints
  reading.py            Reading progress endpoints
  stats.py              Statistics endpoint
services/
  reading_service.py    Reading list business logic
  stats_service.py      Statistics calculations
seed_data.py            Database seed script
```

## Milestones

- **Milestone 1: Reproduce the bugs** — Verified the seeded API responses for Alex and identified that the streak stat and reading history order were both incorrect.
- **Milestone 2: Diagnose Bug 1** — Compared the streak docstring contract with the implementation and confirmed the streak logic was using the wrong field for its date calculation.
- **Milestone 3: Fix Bug 1** — Updated the streak calculation to use finished dates, and confirmed the streak now matches the expected value while the other stats remain correct.
- **Milestone 4: Fix Bug 2** — Traced the history endpoint to the reading service query and updated the ordering to use most recently finished books first.
- **Optional challenge: Add tests** — Added pytest regression tests for streak calculation and history ordering using an in-memory SQLite database.

## Running example requests

After seeding, use `curl` or any HTTP client. The seed script prints all three user IDs — use them in the examples below:

```bash
# Get all books
curl http://127.0.0.1:5000/books/

# Get alex's stats (replace USER_ID with the ID printed by seed_data.py)
curl http://127.0.0.1:5000/stats/USER_ID

# Get alex's reading history
curl http://127.0.0.1:5000/reading/history/USER_ID
```
