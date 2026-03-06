import datetime
import json
from unittest.mock import MagicMock, patch

from django.test import TestCase

from trips.models import ItineraryItem, Trip
from trips.services.ai import generate_itinerary_items
from trips.services.itinerary import build_itinerary


class GenerateItineraryItemsTests(TestCase):
    @patch("trips.services.ai._get_client")
    def test_returns_parsed_list_on_valid_json_response(self, mock_get_client):
        expected = [{"day": 1, "time": "10:00", "activity": "Arrive", "notes": "T5"}]
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.chat.completions.create.return_value.choices[
            0
        ].message.content = json.dumps(expected)

        result = generate_itinerary_items(
            "London", "2025-07-01", "2025-07-03", "3000 USD", "Conference"
        )

        self.assertEqual(result, expected)

    @patch("trips.services.ai._get_client")
    def test_raises_value_error_on_non_json_response(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.chat.completions.create.return_value.choices[
            0
        ].message.content = "Sorry, I cannot help with that."

        with self.assertRaises(ValueError, msg="Should raise when content is not JSON"):
            generate_itinerary_items(
                "London", "2025-07-01", "2025-07-03", "3000 USD", "Conference"
            )

    @patch("trips.services.ai._get_client")
    def test_raises_value_error_when_response_is_not_array(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.chat.completions.create.return_value.choices[
            0
        ].message.content = json.dumps({"day": 1, "activity": "Meeting"})

        with self.assertRaises(ValueError, msg="Should raise when JSON is an object, not array"):
            generate_itinerary_items(
                "London", "2025-07-01", "2025-07-03", "3000 USD", "Conference"
            )

    @patch("trips.services.ai._get_client")
    def test_passes_correct_destination_in_prompt(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.chat.completions.create.return_value.choices[
            0
        ].message.content = json.dumps([])

        generate_itinerary_items("Tokyo", "2025-08-01", "2025-08-04", "5000 USD", "Summit")

        call_kwargs = mock_client.chat.completions.create.call_args
        user_message = call_kwargs.kwargs["messages"][1]["content"]
        self.assertIn("Tokyo", user_message)


class BuildItineraryTests(TestCase):
    def _make_trip(self) -> Trip:
        return Trip.objects.create(
            destination="Tokyo",
            start_date=datetime.date(2025, 8, 1),
            end_date=datetime.date(2025, 8, 4),
            budget="5000.00",
            budget_currency="USD",
            purpose="Partner summit",
        )

    @patch("trips.services.itinerary.generate_itinerary_items")
    def test_creates_and_returns_itinerary_items(self, mock_generate):
        mock_generate.return_value = [
            {"day": 1, "time": "08:00", "activity": "Depart SFO", "notes": ""},
            {"day": 1, "time": "20:00", "activity": "Arrive Narita", "notes": "Terminal 1"},
        ]
        trip = self._make_trip()

        result = build_itinerary(trip)

        self.assertEqual(len(result), 2)
        self.assertEqual(ItineraryItem.objects.filter(trip=trip).count(), 2)

    @patch("trips.services.itinerary.generate_itinerary_items")
    def test_skips_items_missing_required_keys(self, mock_generate):
        mock_generate.return_value = [
            {"day": 1, "time": "08:00", "activity": "Valid item", "notes": ""},
            {"day": 2, "notes": "Missing day and activity"},  # invalid
        ]
        trip = self._make_trip()

        result = build_itinerary(trip)

        self.assertEqual(len(result), 1)
        self.assertEqual(ItineraryItem.objects.filter(trip=trip).count(), 1)

    @patch("trips.services.itinerary.generate_itinerary_items")
    def test_notes_defaults_to_empty_string_when_absent(self, mock_generate):
        mock_generate.return_value = [
            {"day": 1, "time": "09:00", "activity": "Keynote"},  # no notes key
        ]
        trip = self._make_trip()

        build_itinerary(trip)

        item = ItineraryItem.objects.get(trip=trip)
        self.assertEqual(item.notes, "")

    @patch("trips.services.itinerary.generate_itinerary_items")
    def test_returns_empty_list_when_all_items_invalid(self, mock_generate):
        mock_generate.return_value = [
            {"notes": "No day, time, or activity"},
        ]
        trip = self._make_trip()

        result = build_itinerary(trip)

        self.assertEqual(result, [])
        self.assertEqual(ItineraryItem.objects.filter(trip=trip).count(), 0)
