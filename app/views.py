from django.utils import timezone
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from app.models import Show, GalleryImage, SliderImage
from django.contrib.auth.models import User
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from api.serializers import ( 
    ShowSerializer, 
    GalleryImageSerializer, 
    SliderImageSerializer, 
    UserSerializer, 
    TicketCreateSerializer, 
    RegisterSerializer, 
    LoginSerializer, 
    ShowTicketsSerializer
    )


class ShowListCreateView(generics.ListCreateAPIView):
    """List all shows or create a new one (admin only)."""

    queryset = Show.objects.all().order_by('-date')
    serializer_class = ShowSerializer

    def get_permissions(self):
        """Allow POST for admins, GET for everyone."""

        if self.request.method == 'POST':
            return [IsAdminUser()]
        return [AllowAny()]


class ShowUpdateView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a show (admin only)."""

    queryset = Show.objects.all()
    serializer_class = ShowSerializer
    permission_classes = [IsAdminUser]

class FutureShows(generics.ListAPIView):
    """List only future shows."""

    serializer_class = ShowSerializer
    def get_queryset(self): # type: ignore
        """Return shows with future dates."""

        return Show.objects.filter(date__gt=timezone.now()).order_by('-date')

class GalleryListCreateView(generics.ListCreateAPIView):
    """List or create gallery images."""

    queryset = GalleryImage.objects.all()
    serializer_class = GalleryImageSerializer
    permission_classes = [AllowAny]

class GalleryListUpdateView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a gallery image (admin only)."""

    queryset = GalleryImage.objects.all()
    serializer_class = GalleryImageSerializer
    permission_classes = [IsAdminUser]

class SliderListCreateView(generics.ListCreateAPIView):
    """List or create slider images."""

    queryset = SliderImage.objects.all()
    serializer_class = SliderImageSerializer
    permission_classes = [AllowAny]

class SliderListUpdateView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a slider image (admin only)."""

    queryset = SliderImage.objects.all()
    serializer_class = SliderImageSerializer
    permission_classes = [IsAdminUser]

class UserDetailView(generics.RetrieveAPIView):
    """Retrieve authenticated user's profile."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self): # type: ignore
        """Return the current logged-in user."""

        return self.request.user


class TicketsView(generics.ListAPIView):
    """List all shows with their related tickets (admin only)."""

    queryset = Show.objects.all().order_by('-date')
    serializer_class = ShowTicketsSerializer
    permission_classes = [IsAdminUser]

    
class ByTicketView(generics.CreateAPIView):
    """Create a new ticket (available for all users)."""

    queryset = Show.objects.all()
    serializer_class = TicketCreateSerializer
    permission_classes = [AllowAny]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    def perform_create(self, serializer):
        """Save ticket and send email after successful creation."""

        ticket = serializer.save() 

        buyer_name = ticket.buyer_name
        buyer_email = ticket.buyer_email
        buyer_phone = ticket.buyer_phone
        show = ticket.show 

        # Email content
        subject = f"Подтверждаем резервацию билета — {show.name}"
        message = (
            f"Здраствуйте, {buyer_name}!\n\n"
            f"Вы успешно зарезервировали билет на спектакль:\n\n"
            f"Название спектакля: {show.name}\n"
            f"Дата: {show.date.strftime('%d.%m.%Y %H:%M')}\n"
            f"Место: {show.place}\n\n"
            f"Ваш email: {buyer_email}\n"
            f"Телефон: {buyer_phone}\n\n"
            f"Спасибо, что выбрали наш театр Треск!\n"
        )

        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [buyer_email],  # send to buyer's email
                fail_silently=False,
            )
        except Exception as e:
            print("Error mail send:", e)

class RegisterView(generics.CreateAPIView):
    """Register a new user."""

    queryset = User.objects.all()
    serializer_class = RegisterSerializer

@method_decorator(csrf_exempt, name='dispatch')   
class LoginView(APIView):
    """Authenticate user and return token."""

    permission_classes = [AllowAny]
    def post(self, request):
        """Handle user login."""
        
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"] # type: ignore
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key, "user": user.username, "email": user.email})
        return Response(serializer.errors, status = status.HTTP_401_UNAUTHORIZED) 


class SendEmailView(APIView):
    """Send an email from visitors."""

    def post(self, request):
        """Handle sending an email."""
        
        name = request.data.get('name')
        message = request.data.get('message')
        email = request.data.get('email')

        #email content
        subject = f"Сообщение от {name}"
        body = f"От: {name}\nEmail: {email}\n Сообщение: {message}"

        try:
            send_mail(
                subject,
                body,
                settings.DEFAULT_FROM_EMAIL,  # от кого
                ["valeriikuiovda@gmail.com"],     # куда
                fail_silently=False,
            )
            return Response({"message": "Письмо успешно отправлено!"})
        except Exception as e:
            return Response({"message": f"Ошибка: {e}"}, status=500)