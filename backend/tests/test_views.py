from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from trips.models import ItineraryItem, Trip

MOCK_ITEMS = [
    {"day": 1, "time": "09:00", "activity": "Fly to destination", "notes": "Book early"},
    {"day": 1, "time": "14:00", "activity": "Hotel check-in", "notes": "Hilton Downtown"},
    {"day": 2, "time": "09:00", "activity": "Client meeting", "notes": "Conference room B"},
]

VALID_PAYLOAD = {
    "destination": "New York, NY",
    "start_date": "2025-06-01",
    "end_date": "2025-06-03",
    "budget": "2500.00",
    "budget_currency": "USD",
    "purpose": "Q2 sales conference",
}


class TripCreateTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("trip-list-create")

    @patch("trips.services.ai.generate_itinerary_items")
    def test_create_trip_returns_201_with_itinerary(self, mock_generate):
        mock_generate.return_value = MOCK_ITEMS

        response = self.client.post(self.url, data=VALID_PAYLOAD, format="json")

        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data["destination"], "New York, NY")
        self.assertEqual(len(data["itinerary_items"]), 3)
        self.assertEqual(data["itinerary_items"][0]["activity"], "Fly to destination")

    @patch("trips.services.ai.generate_itinerary_items")
    def test_create_trip_persists_to_database(self, mock_generate):
        mock_generate.return_value = MOCK_ITEMS

        self.client.post(self.url, data=VALID_PAYLOAD, format="json")

        self.assertEqual(Trip.objects.count(), 1)
        self.assertEqual(ItineraryItem.objects.count(), 3)

    def test_create_trip_rejects_end_date_before_start_date(self):
        payload = {**VALID_PAYLOAD, "start_date": "2025-06-05", "end_date": "2025-06-01"}

        response = self.client.post(self.url, data=payload, format="json")

        self.assertEqual(response.status_code, 400)

    def test_create_trip_rejects_missing_required_fields(self):
        response = self.client.post(self.url, data={"destination": "Paris"}, format="json")

        self.assertEqual(response.status_code, 400)

    @patch("trips.services.ai.generate_itinerary_items")
    def test_create_trip_rolls_back_and_returns_502_when_ai_fails(self, mock_generate):
        mock_generate.side_effect = ValueError("OpenAI unavailable")

        response = self.client.post(self.url, data=VALID_PAYLOAD, format="json")

        self.assertEqual(response.status_code, 502)
        self.assertEqual(Trip.objects.count(), 0)


class TripListTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("trip-list-create")

    @patch("trips.services.ai.generate_itinerary_items")
    def test_list_returns_all_trips(self, mock_generate):
        mock_generate.return_value = MOCK_ITEMS
        self.client.post(self.url, data=VALID_PAYLOAD, format="json")
        self.client.post(
            self.url,
            data={**VALID_PAYLOAD, "destination": "Chicago, IL"},
            format="json",
        )

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

    def test_list_returns_empty_list_when_no_trips(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])


class TripDetailTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    @patch("trips.services.ai.generate_itinerary_items")
    def test_retrieve_trip_includes_itinerary_items(self, mock_generate):
        mock_generate.return_value = MOCK_ITEMS
        create_resp = self.client.post(
            reverse("trip-list-create"), data=VALID_PAYLOAD, format="json"
        )
        trip_id = create_resp.json()["id"]

        response = self.client.get(reverse("trip-detail", kwargs={"pk": trip_id}))

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["id"], trip_id)
        self.assertEqual(len(data["itinerary_items"]), 3)

    def test_retrieve_nonexistent_trip_returns_404(self):
        response = self.client.get(reverse("trip-detail", kwargs={"pk": 99999}))

        self.assertEqual(response.status_code, 404)
