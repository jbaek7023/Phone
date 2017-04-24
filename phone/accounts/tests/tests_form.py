from django.test import TestCase

from accounts.models import MyUser, UserActivationProfile
from accounts.forms import UserLoginForm, UserCreationForm
# Create your tests here.

# To run test cases
# $ python manage.py test
class FormTestCase(TestCase):
    def setUp(self):
        MyUser.objects.create(
            username='jasonijj',
        email = 'jasondd@gmail.com',
        phone_number = '01098972020',
        password = '0493037333')

    def test_creation_form_valid(self):
        '''
        User can create unique and valid form
        :return:
        '''
        data = {
            'username': 'joystick',
            'email': 'joystcik@gmail.com',
            'phone_number': '01049392222',
            'password1': '!adkdkd33',
            'password2': '!adkdkd33'}
        form = UserCreationForm(data=data)
        self.assertTrue(form.is_valid())

    def test_creation_form_invalid(self):
        '''
        User Can't Create duplicate User
        :return:
        '''

        obj = MyUser.objects.get(email='jasondd@gmail.com')
        data = {
            'username': obj.username,
            'email': obj.email,
            'phone_number': obj.phone_number,
            'password1': obj.password,
            'password2': obj.password}
        form = UserCreationForm(data=data)
        self.assertFalse(form.is_valid())

