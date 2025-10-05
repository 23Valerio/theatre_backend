from rest_framework import serializers
from app.models import Show, GalleryImage, SliderImage, Ticket
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
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

class TicketSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticket
        fields = ['id', 'show', 'user', 'buyer_name', 'buyer_email', 'buyer_phone', 'created_at']


class ShowTicketsSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(source='show_tickets', many=True, read_only=True)
    show_name = serializers.CharField(source='name', read_only=True)
    show_date = serializers.DateTimeField(source='date', read_only=True)

    class Meta:
        model = Show
        fields = ['id', 'show_name', 'show_date',  'tickets_count', 'tickets']

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

class UserSerializer(serializers.ModelSerializer):
    tickets = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'tickets']

    def get_tickets(self, obj):
        from app.models import Ticket
        tickets = Ticket.objects.filter(user=obj).order_by('-bought_at') 
        return TicketSerializer(tickets, many=True).data

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password", "email"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate_username(self, value):
        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError("This login is already used.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("This email is already used.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        return user
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data): # type: ignore
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