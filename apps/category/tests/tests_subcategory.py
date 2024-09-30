from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError

from ..models import Category, SubCategory


class SubCategoryModelTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Test Category")

    def test_subcategory_creation(self):
        subcategory = SubCategory.objects.create(name="Test Subcategory", parent=self.category)

        self.assertEqual(subcategory.name, "Test Subcategory")
        self.assertEqual(str(subcategory), f"Name: {subcategory.name}")

    def test_create_subcategory_non_alphanumeric_name(self):
        with self.assertRaises(ValidationError):
            subcategory = SubCategory(name='Invalid Subcategory!')
            subcategory.full_clean()

    def test_create_subcategory_with_order(self):
        subcategory = SubCategory.objects.create(name='TestSubCategory', order=1, parent=self.category)
        self.assertEqual(subcategory.order, 1)

    def test_create_subcategory_without_parent(self):
        subcategory = SubCategory.objects.create(name='OrphanSubCategory')
        self.assertIsNone(subcategory.parent)

    def test_create_duplicate_subcategory(self):
        SubCategory.objects.create(name='TestSubCategory', parent=self.category)
        with self.assertRaises(IntegrityError):
            SubCategory.objects.create(name='TestSubCategory', parent=self.category)

    def test_subcategory_ordering(self):
        subcategory1 = SubCategory.objects.create(name='TestSubCategory1', order=2, parent=self.category)
        subcategory2 = SubCategory.objects.create(name='TestSubCategory2', order=1, parent=self.category)
        subcategories = SubCategory.objects.all()
        self.assertEqual(subcategories[0], subcategory2)
        self.assertEqual(subcategories[1], subcategory1)

    def test_str_method(self):
        subcategory = SubCategory.objects.create(name="Test Subcategory", parent=self.category)
        expected_str = f"Name: {subcategory.name}"
        self.assertEqual(str(subcategory), expected_str)

    def test_parent_foreign_key(self):
        subcategory = SubCategory.objects.create(name="Test Subcategory", parent=self.category)

        retrieved_subcategory = SubCategory.objects.get(name="Test Subcategory")
        self.assertEqual(retrieved_subcategory.parent, self.category)
