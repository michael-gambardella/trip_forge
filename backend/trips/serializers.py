from rest_framework import serializers

from .models import ItineraryItem, Trip


class ItineraryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItineraryItem
        fields = ["id", "day", "time", "activity", "notes"]


class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = [
            "id",
            "destination",
            "start_date",
            "end_date",
            "budget",
            "budget_currency",
            "purpose",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]

    def validate(self, data: dict) -> dict:
        if data["end_date"] < data["start_date"]:
            raise serializers.ValidationError(
                {"end_date": "end_date must be on or after start_date."}
            )
        return data


class TripDetailSerializer(serializers.ModelSerializer):
    itinerary_items = ItineraryItemSerializer(many=True, read_only=True)

    class Meta:
        model = Trip
        fields = [
            "id",
            "destination",
            "start_date",
            "end_date",
            "budget",
            "budget_currency",
            "purpose",
            "created_at",
            "itinerary_items",
        ]
        read_only_fields = ["id", "created_at"]
