from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from app.views import ShowListCreateView, GalleryListCreateView, ShowUpdateView, SliderListCreateView, GalleryListUpdateView, SliderListUpdateView, UserDetailView, ByTicketView, FutureShows, RegisterView, LoginView, TicketsView
from django.conf import settings
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login/', LoginView.as_view(), name="login"),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/userprofile/', UserDetailView.as_view(), name='user-detail'),
    path('api/shows/', ShowListCreateView.as_view(), name='show-list-create'),
    path('api/shows/<int:pk>/', ShowUpdateView.as_view(), name='update-show'),
    path('api/shows/future/', FutureShows.as_view(), name='future-shows'),
    path('api/gallery/', GalleryListCreateView.as_view(), name='gallery-list-create'),
    path('api/gallery/<int:pk>/', GalleryListUpdateView.as_view(), name='gallery-list-update'),
    path('api/slider/', SliderListCreateView.as_view(), name='slider-list-create'),
    path('api/slider/<int:pk>/', SliderListUpdateView.as_view(), name='slider-list-update'),
    path('api/buyticket/', ByTicketView.as_view(), name='buy-ticket'),
    path('api/tickets/', TicketsView.as_view(), name='tickets'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
