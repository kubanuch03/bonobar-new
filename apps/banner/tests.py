from django.test import TestCase
from apps.category.models import Category 

class BannerTestCase(TestCase):
    def setUp(self) -> None:
        self.category = Category

