from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from app.views import ( 
    ShowListCreateView, 
    GalleryListCreateView, 
    ShowUpdateView, 
    SliderListCreateView, 
    GalleryListUpdateView, 
    SliderListUpdateView, 
    UserDetailView, 
    ByTicketView, 
    FutureShows, 
    RegisterView, 
    LoginView, 
    TicketsView,
    SendEmailView
)

urlpatterns = [
    path('admin/django/', admin.site.urls),
    path('login/', LoginView.as_view(), name="login"),
    path('register/', RegisterView.as_view(), name='register'),
    path('userprofile/', UserDetailView.as_view(), name='user-detail'),
    path('shows/', ShowListCreateView.as_view(), name='show-list-create'),
    path('shows/<int:pk>/', ShowUpdateView.as_view(), name='update-show'),
    path('shows/future/', FutureShows.as_view(), name='future-shows'),
    path('gallery/', GalleryListCreateView.as_view(), name='gallery-list-create'),
    path('gallery/<int:pk>/', GalleryListUpdateView.as_view(), name='gallery-list-update'),
    path('slider/', SliderListCreateView.as_view(), name='slider-list-create'),
    path('slider/<int:pk>/', SliderListUpdateView.as_view(), name='slider-list-update'),
    path('buyticket/', ByTicketView.as_view(), name='buy-ticket'),
    path('tickets/', TicketsView.as_view(), name='tickets'),
    path('sendmail/', SendEmailView.as_view(), name='send_email'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
