import logging

from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Trip
from .serializers import TripDetailSerializer, TripSerializer
from .services.itinerary import build_itinerary

logger = logging.getLogger(__name__)


class TripListCreateView(ListCreateAPIView):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer

    def create(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        trip = serializer.save()

        try:
            build_itinerary(trip)
        except Exception as exc:
            logger.error("Itinerary generation failed for trip %d: %s", trip.id, exc)
            trip.delete()
            return Response(
                {"detail": "Failed to generate itinerary. Please try again."},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        return Response(
            TripDetailSerializer(trip).data, status=status.HTTP_201_CREATED
        )


class TripDetailView(RetrieveAPIView):
    queryset = Trip.objects.prefetch_related("itinerary_items")
    serializer_class = TripDetailSerializer
