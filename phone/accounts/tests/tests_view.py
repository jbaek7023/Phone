from django.test import TestCase
from django.core.urlresolvers import reverse
from django.utils.text import slugify
from accounts.models import MyUser, UserActivationProfile
from accounts.forms import UserLoginForm, UserCreationForm
# Create your tests here.

# To run test cases
# $ python manage.py test
class ViewTestCase(TestCase):
    def test_main_view(self):
        '''
        Testing Main View
        :return:
        '''
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)