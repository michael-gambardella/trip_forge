import logging

from ..models import ItineraryItem, Trip
from .ai import generate_itinerary_items

logger = logging.getLogger(__name__)

_REQUIRED_KEYS = {"day", "time", "activity"}


def build_itinerary(trip: Trip) -> list[ItineraryItem]:
    """Generate and persist itinerary items for a trip.

    Calls the AI service, validates each item, bulk-inserts valid rows,
    and returns the saved ItineraryItem instances.
    """
    raw_items = generate_itinerary_items(
        destination=trip.destination,
        start_date=str(trip.start_date),
        end_date=str(trip.end_date),
        budget=f"{trip.budget} {trip.budget_currency}",
        purpose=trip.purpose,
    )

    to_create: list[ItineraryItem] = []
    for idx, raw in enumerate(raw_items):
        missing = _REQUIRED_KEYS - raw.keys()
        if missing:
            logger.warning(
                "Skipping item %d for trip %d — missing keys: %s",
                idx,
                trip.id,
                missing,
            )
            continue

        to_create.append(
            ItineraryItem(
                trip=trip,
                day=int(raw["day"]),
                time=str(raw["time"]),
                activity=str(raw["activity"]),
                notes=str(raw.get("notes", "")),
            )
        )

    created = ItineraryItem.objects.bulk_create(to_create)
    logger.info("Created %d itinerary items for trip %d", len(created), trip.id)
    return created
