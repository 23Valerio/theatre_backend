from django.utils import timezone
from urllib import response
from rest_framework import generics
from rest_framework.permissions import IsAdminUser, AllowAny
from app.models import Show, GalleryImage, SliderImage
from api.serializers import ShowSerializer, GalleryImageSerializer, SliderImageSerializer, UserSerializer, TicketCreateSerializer
from django.contrib.auth.models import User

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
    permission_classes = [IsAdminUser]

    def get_object(self): # type: ignore
        return self.request.user
    
class ByTicketView(generics.CreateAPIView):
    queryset = Show.objects.all()
    serializer_class = TicketCreateSerializer
    permission_classes = [AllowAny]