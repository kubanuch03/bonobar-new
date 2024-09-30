from django.test import TestCase, Client
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core import cache
from rest_framework.test import APIClient
from rest_framework import status

from ..models import Category


class CategoryModelTestCase(TestCase):
    def test_category_creation(self):
        category = Category.objects.create(name="Test Category")

        self.assertEqual(category.name, "Test Category")
        self.assertEqual(category.created_at.date(), category.created_at.date())

    def test_str_method(self):
        category = Category.objects.create(name="Test Category")
        expected_str = f"Name: {category.name}"
        self.assertEqual(str(category), expected_str)

    def test_verbose_name_plural(self):
        self.assertEqual(Category._meta.verbose_name_plural, "Categories")

    def test_create_category_non_alphanumeric_name(self):
        with self.assertRaises(ValidationError):
            category = Category(name='Invalid Name!')
            category.full_clean()

    def test_create_category_with_image(self):
        category = Category.objects.create(name='TestCategory',
                                           image='category_pictures/2024/07/16/6-830x553-300x200.jpg')
        self.assertEqual(category.image, 'category_pictures/2024/07/16/6-830x553-300x200.jpg')

    def test_create_duplicate_category(self):
        Category.objects.create(name='TestCategory')
        with self.assertRaises(IntegrityError):
            Category.objects.create(name='TestCategory')


class CategoryListViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        Category.objects.create(name='TestCategory1')
        Category.objects.create(name='TestCategory2', image=SimpleUploadedFile(name='test_image.jpg', content=b'',
                                                                               content_type='image/jpeg'))

    def test_category_list(self):
        response = self.client.get(reverse('category:category_list_or_create'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)
        self.assertEqual(response.json()[0]['name'], 'TestCategory1')
        self.assertEqual(response.json()[1]['name'], 'TestCategory2')
        self.assertIsNone(response.json()[0]['image'])
        self.assertIsNotNone(response.json()[1]['image'])
