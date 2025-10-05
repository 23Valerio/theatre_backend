from django.utils import timezone
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from app.models import Show, GalleryImage, SliderImage, Ticket
from api.serializers import ShowSerializer, GalleryImageSerializer, SliderImageSerializer, UserSerializer, TicketCreateSerializer, RegisterSerializer, LoginSerializer, TicketSerializer, ShowTicketsSerializer
from django.contrib.auth.models import User
from rest_framework import status

class ShowListCreateView(generics.ListCreateAPIView):
    queryset = Show.objects.all().order_by('-date')
    serializer_class = ShowSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser()]
        return [AllowAny()]

class ShowDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Show.objects.all()
    serializer_class = ShowSerializer
    permission_classes = [IsAdminUser]

class ShowUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Show.objects.all()
    serializer_class = ShowSerializer
    permission_classes = [IsAdminUser]

class FutureShows(generics.ListAPIView):
    serializer_class = ShowSerializer
    def get_queryset(self): # type: ignore
        return Show.objects.filter(date__gt=timezone.now()).order_by('-date')

class GalleryListCreateView(generics.ListCreateAPIView):
    queryset = GalleryImage.objects.all()
    serializer_class = GalleryImageSerializer
    permission_classes = [AllowAny]

class GalleryListUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = GalleryImage.objects.all()
    serializer_class = GalleryImageSerializer
    permission_classes = [IsAdminUser]

class SliderListCreateView(generics.ListCreateAPIView):
    queryset = SliderImage.objects.all()
    serializer_class = SliderImageSerializer
    permission_classes = [AllowAny]

class SliderListUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SliderImage.objects.all()
    serializer_class = SliderImageSerializer
    permission_classes = [IsAdminUser]

class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self): # type: ignore
        return self.request.user


# !!!!!!! 
class TicketsView(generics.ListAPIView):
    queryset = Show.objects.all().order_by('-date')
    serializer_class = ShowTicketsSerializer
    permission_classes = [IsAdminUser]

    
class ByTicketView(generics.CreateAPIView):
    queryset = Show.objects.all()
    serializer_class = TicketCreateSerializer
    permission_classes = [AllowAny]

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"] # type: ignore
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
        return Response(serializer.errors, status = status.HTTP_401_UNAUTHORIZED) 
