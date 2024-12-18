from rest_framework.test import APITestCase

from common import models


class AboutUsApiTestCase(APITestCase):
    def test_about_us_api(self):
        title = 'title 1'
        description = 'description1'
        image = 'test.png'
        for _ in range(5):
            models.AboutUs.objects.create(
                title=title,
                description=description,
                media=image
            )
        response = self.client.get('/api/v1/common/about-us/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 5)


class AdvertisementApiTestCase(APITestCase):
    def test_advertisement_api(self):
        image_uz = 'test.png'
        image_ru = 'ru.png'
        for _ in range(5):
            models.Advertisement.objects.create(
                image_uz=image_uz, image_ru=image_ru
            )

        response = self.client.get('/api/v1/common/advertisement/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 5)


class BannerApiTestCase(APITestCase):
    def test_banner_api(self):
        image_uz = 'test.png'
        image_ru = 'ru.png'
        for _ in range(5):
            models.Banner.objects.create(
                image_uz=image_uz, image_ru=image_ru
            )

        response = self.client.get('/api/v1/common/banner/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 5)


