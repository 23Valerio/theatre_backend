from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

class Show(models.Model):
    """Model representing a theater show."""

    name = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateTimeField()
    place = models.CharField(max_length=100, default='Divadlo Kámen')
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='show_images/', null=True, blank=True)
    tickets_count = models.PositiveIntegerField(default=100)
    tickets = models.ManyToManyField(User, through='Ticket', related_name='shows', blank=True)

    def clean(self):
        """Validate that the show date is not in the past."""

        if self.date < timezone.now():
            raise ValidationError("Show date cannot be in the past.")

    def __str__(self):
        """Return a readable show representation."""

        return f"{self.name} - {self.date.strftime('%Y-%m-%d %H:%M')}"

 
class Ticket(models.Model):
    """Model representing a purchased ticket."""

    show = models.ForeignKey(Show, related_name='show_tickets', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='show_tickets', on_delete=models.CASCADE, null=True, blank=True)
    buyer_name = models.CharField(max_length=100, default="Ivan")
    buyer_email = models.EmailField(blank=True, default="unknown@example.com")
    buyer_phone = models.CharField(max_length=15, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return a readable ticket representation."""
        return f"{self.show.name} {self.show.date.strftime('%Y-%m-%d')} buyer {self.buyer_name}" 

class SliderImage(models.Model):
    """Model for images used in the homepage slider."""

    image = models.ImageField(upload_to='slider_images/', blank=True)


class GalleryImage(models.Model):
    """Model for images displayed in the gallery."""

    image = models.ImageField(upload_to='gallery_images/', blank=True)

