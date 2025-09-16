from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

class Show(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateTimeField()
    place = models.CharField(max_length=100, default='Divadlo Kámen')
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='show_images/', null=True, blank=True)
    tickets_count = models.PositiveIntegerField(default=100)
    tickets = models.ManyToManyField(User, through='Ticket', related_name='shows', blank=True)

    def clean(self):
        if self.date < timezone.now():
            raise ValidationError("Show date cannot be in the past.")

    def __str__(self):
        return f"{self.name} - {self.date.strftime('%Y-%m-%d %H:%M')}"

 
class Ticket(models.Model):
    show = models.ForeignKey(Show, related_name='show_tickets', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='show_tickets', on_delete=models.CASCADE, null=True, blank=True)
    buyer_name = models.CharField(max_length=100, blank=True, null=True)
    buyer_email = models.EmailField(blank=True, null=True)
    buyer_phone = models.CharField(max_length=15, blank=True, null=True)
    bought_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.show.name} {self.show.date.strftime('%Y-%m-%d')} buyer {self.buyer_name}" 

class SliderImage(models.Model):
    image = models.ImageField(upload_to='slider_images/', blank=True)

class GalleryImage(models.Model):
    image = models.ImageField(upload_to='gallery_images/', blank=True)