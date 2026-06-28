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

- Milestone 1:
  -  Read the Codebase — Traced the call chain from the stats route through the service layer to the model. Identified that calculate_streak() and get_reading_history() both depend on reading event date fields, and noted what get_reading_history() guarantees about the events it returns.

- Milestone 2:
  - See Both Bugs in Action — Hit the stats and history endpoints for alex, confirmed reading_streak returned 0, and noted the history came back in the wrong order. Calculated the expected streak value from the finished dates to use as a verification target.

- Milestone 3:
  - Trace and Fix Bug 1 — Compared the calculate_streak() docstring against the implementation and found it was using started_at where the contract specified finished_at. Changed one field reference and confirmed the streak matched the expected value with other stats unchanged.

- Milestone 4:
  - Trace and Fix Bug 2 — Traced the history endpoint to get_reading_history() and found the order_by clause used started_at instead of finished_at. Fixed the ordering and confirmed that history now returns the most recently finished first across multiple users.

- Optional:
  -  Added regression tests — Added pytest tests covering streak calculation and history ordering using an in-memory SQLite database.



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
