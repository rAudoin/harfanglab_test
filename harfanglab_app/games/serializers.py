from rest_framework import serializers
from .models import Game, Platform


class PlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platform
        fields = "__all__"


class GameSerializer(serializers.ModelSerializer):
    platforms = serializers.SlugRelatedField(
        many=True, slug_field="name", queryset=Platform.objects.all()
    )

    class Meta:
        model = Game
        fields = "__all__"

    def validate_name(self, value):
        """Validate game name, not empty"""
        if not value or not value.strip():
            raise serializers.ValidationError("Game name cannot be empty.")
        return value.strip()

    def validate_ratings(self, value):
        """Validate rating, between 0 anf 20"""
        if value < 0 or value > 20:
            raise serializers.ValidationError("Rating must be between 0 and 20.")
        return value

    def validate_platforms(self, value):
        """Validate platforms, platforms must exist"""
        if not value:
            raise serializers.ValidationError("At least one platform is required.")
        return value

    def create(self, validated_data):
        """Create game with existing platforms only"""
        platforms = validated_data.pop("platforms", [])
        game = Game.objects.create(**validated_data)

        # Associate existing platforms
        game.platforms.set(platforms)

        return game

    def update(self, instance, validated_data):
        """Game update"""
        platforms = validated_data.pop("platforms", None)

        # Update simple fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update platforms
        if platforms is not None:
            instance.platforms.set(platforms)

        return instance
