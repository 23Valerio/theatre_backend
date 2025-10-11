from django.utils import timezone
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from app.models import Show, GalleryImage, SliderImage
from django.contrib.auth.models import User
from rest_framework import status
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

# class ShowDetailView(generics.RetrieveUpdateDestroyAPIView):
#     """Retrieve, update, or delete a show (admin only)."""

#     queryset = Show.objects.all()
#     serializer_class = ShowSerializer
#     permission_classes = [IsAdminUser]

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

class RegisterView(generics.CreateAPIView):
    """Register a new user."""

    queryset = User.objects.all()
    serializer_class = RegisterSerializer
   
class LoginView(APIView):
    """Authenticate user and return token."""

    def post(self, request):
        """Handle user login."""
        
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"] # type: ignore
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
        return Response(serializer.errors, status = status.HTTP_401_UNAUTHORIZED) 
