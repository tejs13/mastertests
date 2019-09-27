from rest_framework import status
from rest_framework.test import APITestCase
from api.models.country import country
from rest_framework.test import APIClient

from django.contrib.auth.models import User


class CountryTests(APITestCase):
    user = User.objects.get(username='tejas')
    client = APIClient()
    client.force_authenticate(user=user)

    def test_create_country(self):
        url = '/master/api.country'
        for i in range(100):
            data = {'name': 'NewCountry', 'code': 'NWCN'}
            response = self.client.post(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            cntr = country.objects.all().last()
            for field_name in data.keys():
                self.assertEqual(getattr(cntr, field_name), data[field_name])



    def test_get_country(self):
        url = '/master/api.country/list'
        url_post = '/master/api.country'
        cntr = country.objects.all()
        for i in range(100):
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            for c in cntr:
                self.assertEqual(response.data[0]['name'], c.name)
                self.assertEqual(response.data[0]['code'], c.code)

    def test_put_country(self):
        url = '/master/api.country/1'
        url_post = '/master/api.country'
        d = {'code': 'NWWW'}
        data = {'name': 'NewCountry', 'code': 'NWCN'}
        response = self.client.post(url_post, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        cntr = country.objects.all().last()
        response = self.client.put(url, data=d, format='json')
        for i in d.keys():
            self.assertEqual(response.data['code'], d[i])

    def test_delete_country(self):
        url = '/master/api.country/1'
        url_post = '/master/api.country'
        data = {'name': 'NewCountry', 'code': 'NWCN'}
        response = self.client.post(url_post, data, format='json')
        response = self.client.delete(url, format='json', follow=True)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
