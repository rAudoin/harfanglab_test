from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Platform(models.Model):
    """Platform model"""

    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Game(models.Model):
    """Game model"""

    name = models.CharField(max_length=200, blank=False)
    release_date = models.DateField()
    studio = models.CharField(max_length=100)
    ratings = models.IntegerField(
        help_text="Rating out of 20",
        validators=[MinValueValidator(0), MaxValueValidator(20)],
    )
    platforms = models.ManyToManyField(Platform, related_name="games")

    def clean(self):
        if not self.name or not self.name.strip():
            raise ValidationError({"name": "Game name cannot be empty."})

        # Clean name
        if self.name:
            self.name = self.name.strip()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-release_date", "name"]
        unique_together = ["name", "studio"]
