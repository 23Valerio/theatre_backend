from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from app.models import Show, Ticket, GalleryImage, SliderImage
from django.utils import timezone
from datetime import timedelta
from unittest.mock import patch

class UserAuthTests(APITestCase):

    def test_register_user(self):
        url = reverse('register')
        data = {
            'username': 'testuser',
            'password': 'testpass123',
            'email': 'test@example.com'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_login_user(self):
        user = User.objects.create_user(username='testuser', password='testpass123')
        url = reverse('login')
        data = {'username': 'testuser', 'password': 'testpass123'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data) # type: ignore


class ShowTests(APITestCase):

    def setUp(self):
        self.admin = User.objects.create_superuser(username='admin', password='adminpass') # type: ignore
        self.client = APIClient()
        self.show_data = {
            'name': 'Test Show',
            'description': 'Test Description',
            'date': (timezone.now() + timedelta(days=1)).isoformat(),
            'place': 'Test Theater',
            'tickets_count': 10
        }

    def test_create_show_admin_only(self):
        self.client.login(username='admin', password='adminpass')
        url = reverse('show-list-create')
        response = self.client.post(url, self.show_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Show.objects.count(), 1)

    def test_non_admin_cannot_create_show(self):
        user = User.objects.create_user(username='user', password='userpass')
        self.client.login(username='user', password='userpass')
        url = reverse('show-list-create')
        response = self.client.post(url, self.show_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_future_shows(self):
        Show.objects.create(name='Past Show', description='Past', date=timezone.now() - timedelta(days=1))
        future_show = Show.objects.create(name='Future Show', description='Future', date=timezone.now() + timedelta(days=2))
        url = reverse('future-shows')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1) # type: ignore
        self.assertEqual(response.data[0]['name'], future_show.name) # type: ignore


class TicketTests(APITestCase):

    def setUp(self):
        self.show = Show.objects.create(
            name='Show with Tickets',
            description='Desc',
            date=timezone.now() + timedelta(days=2),
            tickets_count=2
        )

    @patch('app.views.send_mail')  # Мок для send_mail
    def test_buy_ticket_reduces_count(self, mock_send_mail):
        url = reverse('buy-ticket')
        data = {
            'show': self.show.id, # type: ignore
            'buyer_name': 'John Doe',
            'buyer_email': 'john@example.com',
            'buyer_phone': '1234567890'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.show.refresh_from_db()
        self.assertEqual(self.show.tickets_count, 1)
        mock_send_mail.assert_called_once()  # Перевіряємо, що лист був "відправлений"

    def test_buy_ticket_when_none_left(self):
        self.show.tickets_count = 0
        self.show.save()
        url = reverse('buy-ticket')
        data = {
            'show': self.show.id, # type: ignore
            'buyer_name': 'Jane Doe',
            'buyer_email': 'jane@example.com',
            'buyer_phone': '0987654321'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserProfileTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='user1', password='pass123')
        self.show = Show.objects.create(
            name='Test Show',
            description='Desc',
            date=timezone.now() + timedelta(days=2),
            tickets_count=5
        )
        Ticket.objects.create(show=self.show, user=self.user, buyer_name='user1', buyer_email='u1@example.com', buyer_phone='123')
        self.client.login(username='user1', password='pass123')

    def test_user_profile_contains_tickets(self):
        url = reverse('user-detail')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['tickets']), 1) # type: ignore
        self.assertEqual(response.data['tickets'][0]['buyer_name'], 'user1')# type: ignore


class GallerySliderTests(APITestCase):

    def setUp(self):
        self.admin = User.objects.create_superuser(username='admin', password='adminpass')# type: ignore
        self.client.login(username='admin', password='adminpass')
        self.gallery_data = {}
        self.slider_data = {}

    def test_create_gallery_image_admin_only(self):
        url = reverse('gallery-list-create')
        response = self.client.post(url, self.gallery_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_slider_image_admin_only(self):
        url = reverse('slider-list-create')
        response = self.client.post(url, self.slider_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
