from rest_framework import serializers
from app.models import Show, GalleryImage, SliderImage, Ticket
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.utils import timezone

class ShowSerializer(serializers.ModelSerializer):
    """Serializer for the Show model."""

    class Meta:
        model = Show
        fields = ['id', 'name', 'description', 'date', 'place', 'created_at', 'image', 'tickets_count']

    def validate_date(self, value):
        """Check that the show date is in the future."""

        if value <= timezone.now():
            raise serializers.ValidationError("The date must be in the future.")
        return value
    
class GalleryImageSerializer(serializers.ModelSerializer):
    """Serializer for gallery images."""

    class Meta:
        model = GalleryImage
        fields = ['id', 'image']

class SliderImageSerializer(serializers.ModelSerializer):
    """Serializer for slider images."""

    class Meta:
        model = SliderImage
        fields = ['id', 'image']

class TicketSerializer(serializers.ModelSerializer):
    """Serializer for the Ticket model."""

    show_name = serializers.CharField(source='show.name', read_only=True)
    show_date = serializers.DateTimeField(source='show.date', read_only=True)
    
    class Meta:
        model = Ticket
        fields = ['id', 'show', 'user', 'buyer_name', 'buyer_email', 'buyer_phone', 'created_at']


class ShowTicketsSerializer(serializers.ModelSerializer):
    """Serializer for shows including related tickets."""

    tickets = TicketSerializer(source='show_tickets', many=True, read_only=True)
    show_name = serializers.CharField(source='name', read_only=True)
    show_date = serializers.DateTimeField(source='date', read_only=True)

    class Meta:
        model = Show
        fields = ['id', 'show_name', 'show_date',  'tickets_count', 'tickets']

class TicketCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating new tickets."""
    class Meta:
        model = Ticket
        fields = ['id', 'show', 'buyer_name', 'buyer_email', 'buyer_phone']

    def create(self, validated_data):
        """Create a new ticket and decrease show's available tickets."""
        request = self.context['request']
        user = request.user if request.user.is_authenticated else None

        show = validated_data['show']

        if show.tickets_count <= 0:
            raise serializers.ValidationError("No tickets available for this show.")
        
        ticket = Ticket.objects.create(user=user, **validated_data)
        show.tickets_count -= 1
        show.save(update_fields=['tickets_count'])
        
        return ticket

class UserSerializer(serializers.ModelSerializer):
    """Serializer for Django User model.

    Includes user details and a list of purchased tickets.
    """
    tickets = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'tickets']

    def get_tickets(self, obj):
        """Retrieve all tickets purchased by the user."""

        from app.models import Ticket
        tickets = Ticket.objects.filter(user=obj).order_by('-created_at') 
        return TicketSerializer(tickets, many=True).data

class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration.

    Handles user creation and ensures unique username and email.
    """
    class Meta:
        model = User
        fields = ["username", "password", "email"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate_username(self, value):
        """Ensure username is unique (case-insensitive)."""
        
        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError("This login is already used.")
        return value

    def validate_email(self, value):
        """Ensure email is unique (case-insensitive)."""

        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("This email is already used.")
        return value

    def create(self, validated_data):
        """Create a new user with hashed password."""

        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        return user
    
class LoginSerializer(serializers.Serializer):
    """Serializer for user login authentication.

    Validates credentials and authenticates the user.
    """
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data): # type: ignore
        """Authenticate user credentials."""
        
        username = data.get("username")
        password = data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError("Wrong login or password.")
        else:
            raise serializers.ValidationError("You must enter both a username and password.")

        data["user"] = user
        return data