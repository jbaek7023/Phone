from django.test import TestCase

from accounts.models import MyUser, UserActivationProfile
# Create your tests here.

# To run test cases
# $ python manage.py test
class UserModelTestCase(TestCase):
    def setUp(self):
        MyUser.objects.create(
            username='jason',
        email = 'jason@gmail.com',
        phone_number = '01098972020',
        password = '0493037333')

    def test_simple_user_model(self):
        '''
        User can register and retrieve user by matching email
        :return:
        '''
        obj = MyUser.objects.get(email='jason@gmail.com')
        self.assertEqual(obj.username, 'jason')
        self.assertEqual(obj.phone_number, '01098972020')
