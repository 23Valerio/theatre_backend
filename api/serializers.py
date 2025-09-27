from rest_framework import serializers
from app.models import Show, GalleryImage, SliderImage, Ticket
from django.contrib.auth.models import User
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

class TicketSerializer(serializers.Serializer):
    show_name = serializers.CharField(source='show.name', read_only=True)
    show_date = serializers.DateTimeField(source='show.date', read_only=True)

    class Meta:
        model = Ticket
        fields = ['id', 'show_name', 'show_date', 'buyer_name', 'buyer_email', 'buyer_phone', 'bought_at']

class TicketCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'show', 'buyer_name', 'buyer_email', 'buyer_phone']

    def create(self, validated_data):
        request = self.context['request']
        user = request.user if request.user.is_authenticated else None

        show = validated_data['show']

        if show.tickets_count <= 0:
            raise serializers.ValidationError("No tickets available for this show.")
        
        ticket = Ticket.objects.create(user=user, **validated_data)
        show.tickets_count -= 1
        show.save(update_fields=['tickets_count'])
        
        return ticket

class UserSerializer(serializers.Serializer):
    tickets = TicketSerializer(source='show_tickets', many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'tickets']