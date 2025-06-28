from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as django_filters
from .models import Game, Platform
from .serializers import GameSerializer, PlatformSerializer


class GameFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")
    studio = django_filters.CharFilter(lookup_expr="icontains")
    release_year = django_filters.NumberFilter(
        field_name="release_date", lookup_expr="year"
    )
    ratings_min = django_filters.NumberFilter(field_name="ratings", lookup_expr="gte")
    ratings_max = django_filters.NumberFilter(field_name="ratings", lookup_expr="lte")
    platform = django_filters.CharFilter(
        field_name="platforms__name", lookup_expr="icontains"
    )

    class Meta:
        model = Game
        fields = [
            "name",
            "studio",
            "release_year",
            "ratings_min",
            "ratings_max",
            "platform",
        ]


class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all().prefetch_related("platforms")  # Avoid N+1 !
    serializer_class = GameSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = GameFilter
    search_fields = ["name", "studio"]
    ordering_fields = ["name", "release_date", "ratings", "created_at"]
    ordering = ["-release_date"]

    @action(detail=False, methods=["get"])
    def by_studio(self, request):
        """Endpoint to list games by studio"""
        studio = request.query_params.get("studio")
        if not studio:
            return Response(
                {"error": "Studio parameter is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        games = self.queryset.filter(studio__icontains=studio)
        serializer = self.get_serializer(games, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def top_rated(self, request):
        """Endpoint for top rated games"""
        min_rating = request.query_params.get("min_rating")
        if not min_rating:
            return Response({"error": "min_rating parameter is required"}, status=400)

        # Cast in integer
        try:
            min_rating = int(min_rating)
        except ValueError:
            return Response(
                {"error": "min_rating must be a valid integer"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        games = self.queryset.filter(ratings__gte=min_rating)
        serializer = self.get_serializer(games, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def by_platform(self, request):
        """Endpoint to list game by platform"""
        platform = request.query_params.get("platform")
        if not platform:
            return Response(
                {"error": "Platform parameter is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        games = self.queryset.filter(platforms__name__icontains=platform)
        serializer = self.get_serializer(games, many=True)
        return Response(serializer.data)


class PlatformViewSet(viewsets.ModelViewSet):
    queryset = Platform.objects.all()
    serializer_class = PlatformSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name"]
    ordering = ["name"]
