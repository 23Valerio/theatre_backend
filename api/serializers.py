from rest_framework import serializers
from app.models import Show, GalleryImage, SliderImage
from django.utils import timezone

class ShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Show
        fields = ['id', 'name', 'description', 'date', 'place', 'created_at', 'image', 'tickets_count']

    def validate_date(self, value):
        if value <= timezone.now():
            raise serializers.ValidationError("The date must be in the future.")
        return value
    
class GalleryImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GalleryImage
        fields = ['id', 'image']

class SliderImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SliderImage
        fields = ['id', 'image']