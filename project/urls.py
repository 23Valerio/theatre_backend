from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from app.views import ShowListCreateView, GalleryListCreateView, ShowUpdateView, SliderListCreateView, GalleryListUpdateView, SliderListUpdateView
from django.conf import settings
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login/', obtain_auth_token, name='api_token_auth'),
    path('api/shows/', ShowListCreateView.as_view(), name='show-list-create'),
    path('api/shows/<int:pk>/', ShowUpdateView.as_view(), name='update-show'),
    path('api/gallery/', GalleryListCreateView.as_view(), name='gallery-list-create'),
    path('api/gallery/<int:pk>/', GalleryListUpdateView.as_view(), name='gallery-list-update'),
    path('api/slider/', SliderListCreateView.as_view(), name='slider-list-create'),
    path('api/slider/<int:pk>/', SliderListUpdateView.as_view(), name='slider-list-update'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
