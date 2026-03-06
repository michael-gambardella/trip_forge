# TripForge

[![CI](https://github.com/michael-gambardella/trip_forge/actions/workflows/ci.yml/badge.svg)](https://github.com/michael-gambardella/trip_forge/actions/workflows/ci.yml)

An AI-powered business travel planner. Input a destination, dates, and budget — TripForge calls the OpenAI API to generate a structured day-by-day itinerary, stores it in PostgreSQL, and serves it through a clean REST API consumed by a React frontend.

## Stack

| Layer | Technology |
|-------|-----------|
| Backend | Django 4.2 + Django REST Framework |
| Database | PostgreSQL 15 |
| AI | OpenAI Chat Completions (`gpt-4o-mini`) |
| Frontend | React 18 + TypeScript (Vite) |
| Infrastructure | Docker Compose |

## Quick Start (Docker)

**Prerequisites:** Docker Desktop

```bash
cp .env.example .env
# Add your OPENAI_API_KEY to .env

docker-compose up --build
```

| Service | URL |
|---------|-----|
| Frontend | http://localhost:5173 |
| Backend API | http://localhost:8000/api/ |
| Django Admin | http://localhost:8000/admin/ |

The backend container runs `migrate` automatically on startup — no manual setup needed.

## Local Development (without Docker)

**Prerequisites:** Python 3.11+, Node 20+, PostgreSQL running locally

```bash
# Backend
cd backend
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp ../.env.example ../.env  # fill in DATABASE_URL and OPENAI_API_KEY
python manage.py migrate
python manage.py runserver

# Frontend (new terminal)
cd frontend
npm install
npm run dev
```

## Running Tests

```bash
cd backend
pip install -r requirements.txt  # if not already installed
pytest
```

The test suite covers all API endpoints and the service layer. **OpenAI is never called during tests** — the `generate_itinerary_items` function is mocked with `unittest.mock.patch`. This keeps the suite fast, free, and deterministic.

## API Reference

### `POST /api/trips/`

Create a trip and generate its itinerary.

**Request body:**
```json
{
  "destination": "New York, NY",
  "start_date": "2025-06-01",
  "end_date": "2025-06-03",
  "budget": "2500.00",
  "budget_currency": "USD",
  "purpose": "Q2 sales conference"
}
```

**Response `201`:**
```json
{
  "id": 1,
  "destination": "New York, NY",
  "start_date": "2025-06-01",
  "end_date": "2025-06-03",
  "budget": "2500.00",
  "budget_currency": "USD",
  "purpose": "Q2 sales conference",
  "created_at": "2025-06-01T10:00:00Z",
  "itinerary_items": [
    { "id": 1, "day": 1, "time": "08:00", "activity": "Fly JFK", "notes": "Terminal 4" },
    ...
  ]
}
```

### `GET /api/trips/` — list all trips
### `GET /api/trips/<id>/` — retrieve a trip with its itinerary

## Architecture Decisions

**Service layer, not fat views.** Business logic lives in `trips/services/`, not in views. `services/ai.py` contains the OpenAI call in isolation — it can be mocked, swapped, or extended (e.g. retries, model fallback) without touching the view. `services/itinerary.py` owns persistence logic. The view stays thin: validate input, call the service, return the response.

**Structured AI output.** The system prompt instructs the model to return a JSON array with a fixed schema (`day`, `time`, `activity`, `notes`). The server parses this, validates required keys, and bulk-inserts rows. This is more reliable than free-text parsing and maps directly to the `ItineraryItem` model.

**Mocked tests, never hitting the API.** Every endpoint test patches `generate_itinerary_items`. This means tests run without an API key, cost nothing, and never flake due to network issues. The service unit tests separately patch the `OpenAI` client constructor to verify parsing and error-handling logic in isolation.

**Typed frontend.** The `ItineraryItem`, `Trip`, `TripDetail`, and `CreateTripPayload` interfaces in `src/api/trips.ts` mirror the Django serializer fields exactly. No `any` types — TypeScript will catch mismatches if the API contract changes.

**Single-command local dev.** `docker-compose up --build` starts Postgres, applies migrations, starts the Django dev server, and serves the Vite frontend — all from one command.
