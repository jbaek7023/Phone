from django.test import TestCase, RequestFactory
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from django.urls import reverse

from accounts.models import MyUser, UserActivationProfile
from accounts.forms import UserLoginForm, UserCreationForm
from accounts.views import user_register, user_login, user_logout

# To run test cases
# $ python manage.py test
User = get_user_model()
class FormTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = MyUser.objects.create(
            username='jasonijj',
            email = 'jasondd@gmail.com',
            phone_number = '01098972020',
            password = '0493037333'
        )

    def test_user_login(self):
        '''
        Test Login
        :return:
        '''
        login_url = reverse("login")
        request = self.factory.get(login_url)
        request.user = self.user

        response = user_login(request)
        self.assertEqual(response.status_code, 200)
