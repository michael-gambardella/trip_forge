from django.db import models


class Trip(models.Model):
    destination = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    budget_currency = models.CharField(max_length=3, default="USD")
    purpose = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.destination} ({self.start_date} – {self.end_date})"


class ItineraryItem(models.Model):
    trip = models.ForeignKey(
        Trip, on_delete=models.CASCADE, related_name="itinerary_items"
    )
    day = models.PositiveIntegerField()
    # Stored as HH:MM (zero-padded, 24-hour). The AI prompt enforces this format;
    # lexicographic ordering is only correct when times are consistently zero-padded.
    time = models.CharField(max_length=10)
    activity = models.CharField(max_length=500)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["day", "time"]

    def __str__(self) -> str:
        return f"Day {self.day} {self.time}: {self.activity}"
