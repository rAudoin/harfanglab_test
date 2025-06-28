from django.core.management.base import BaseCommand
from games.models import Game, Platform
from datetime import date


class Command(BaseCommand):
    help = "Load sample data"

    def handle(self, *args, **options):
        platforms_data = ["PC", "PS4", "PS5", "Switch", "One", "WiiU", "PS3"]
        platforms = {}

        for platform_name in platforms_data:
            platform, created = Platform.objects.get_or_create(name=platform_name)
            platforms[platform_name] = platform
            if created:
                self.stdout.write(f"Platform created: {platform_name}")

        games_data = [
            {
                "name": "The Witcher 3 : Wild Hunt",
                "release_date": date(2015, 5, 19),
                "studio": "CD Projekt RED",
                "ratings": 19,
                "platforms": ["PC", "PS4", "PS5", "Switch", "One"],
            },
            {
                "name": "Mario Kart 8 Deluxe",
                "release_date": date(2017, 4, 28),
                "studio": "Nintendo",
                "ratings": 16,
                "platforms": ["Switch"],
            },
            {
                "name": "Don't Starve",
                "release_date": date(2013, 4, 23),
                "studio": "Capybara Games",
                "ratings": 17,
                "platforms": ["PC", "PS4", "Switch", "One", "WiiU", "PS3"],
            },
        ]

        for game_data in games_data:
            platform_names = game_data.pop("platforms")
            game, created = Game.objects.get_or_create(
                name=game_data["name"], studio=game_data["studio"], defaults=game_data
            )

            if created:
                for platform_name in platform_names:
                    game.platforms.add(platforms[platform_name])
                self.stdout.write(f"Game created: {game.name}")
            else:
                self.stdout.write(f"Game already exists: {game.name}")

        self.stdout.write(self.style.SUCCESS("Sample data loaded successfully!"))
