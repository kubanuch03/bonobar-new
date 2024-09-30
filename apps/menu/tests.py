from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Menu
from apps.category.models import Category, SubCategory


class MenuModelTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Test Category")
        self.subcategory = SubCategory.objects.create(name="Test Subcategory", parent=self.category)

    def test_menu_creation(self):
        menu = Menu.objects.create(
            title="Test Menu",
            price=100,
            image=SimpleUploadedFile("test_image.jpg", b""),
            description="Test description",
            category=self.category,
            subcategory=self.subcategory
        )

        self.assertEqual(menu.title, "Test Menu")
        self.assertEqual(menu.price, 100)
        self.assertEqual(menu.description, "Test description")
        self.assertEqual(menu.category, self.category)
        self.assertEqual(menu.subcategory, self.subcategory)
        self.assertEqual(str(menu), f"Menu: {menu.title}, price: {menu.price}")

    def test_str_method(self):
        menu = Menu.objects.create(
            title="Test Menu",
            price=100,
            image=SimpleUploadedFile("test_image.jpg", b""),
            description="Test description",
            category=self.category,
            subcategory=self.subcategory
        )
        expected_str = f"Menu: {menu.title}, price: {menu.price}"
        self.assertEqual(str(menu), expected_str)

    def test_blank_description(self):
        menu = Menu.objects.create(
            title="Test Menu",
            price=100,
            image=SimpleUploadedFile("test_image.jpg", b""),
            category=self.category,
            subcategory=self.subcategory
        )
        self.assertIsNone(menu.description)
