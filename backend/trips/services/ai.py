import json
import logging

from django.conf import settings
from openai import OpenAI

logger = logging.getLogger(__name__)

_SYSTEM_PROMPT = (
    "You are a professional business travel planner. "
    "Generate a detailed day-by-day itinerary for a business trip. "
    "Respond ONLY with a valid JSON array. "
    "Do not include markdown, code fences, or any text outside the JSON. "
    "Each element must be an object with exactly these keys: "
    '"day" (integer, starting at 1), '
    '"time" (string, HH:MM 24-hour format), '
    '"activity" (string, concise description), '
    '"notes" (string, practical details such as addresses, booking tips, or reminders). '
    "Order items chronologically within each day. "
    "Include flights, hotel check-in, meals, meetings, and relevant sightseeing."
)


def generate_itinerary_items(
    destination: str,
    start_date: str,
    end_date: str,
    budget: str,
    purpose: str,
) -> list[dict]:
    """Call the OpenAI Chat Completions API and return a list of raw item dicts.

    Each dict contains: day (int), time (str), activity (str), notes (str).

    Raises:
        ValueError: if the API response is not a valid JSON array.
    """
    client = OpenAI(api_key=settings.OPENAI_API_KEY)

    user_prompt = (
        f"Plan a business trip to {destination}.\n"
        f"Dates: {start_date} to {end_date}.\n"
        f"Budget: {budget}.\n"
        f"Purpose: {purpose or 'General business travel'}.\n"
        "Return the full itinerary as a JSON array."
    )

    response = client.chat.completions.create(
        model=settings.OPENAI_MODEL,
        messages=[
            {"role": "system", "content": _SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.7,
    )

    raw = response.choices[0].message.content.strip()
    logger.debug("OpenAI raw response: %s", raw[:500])

    try:
        items = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"OpenAI returned non-JSON content: {raw[:200]}"
        ) from exc

    if not isinstance(items, list):
        raise ValueError(
            f"Expected a JSON array from OpenAI, got: {type(items).__name__}"
        )

    return items
