from django.test import TestCase
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.utils.text import slugify

from .models import Product, Category

class ProductTestCase(TestCase):

    def setUp(self):
        Category.objects.create(name = 'CayegoryName')
        user = User.objects.create_user('UserName', password='start1234')
        self.products_count = 15
        for i in range(0, self.products_count):
            Product.objects.create(user = user, 
            name  = 'ProductName',
            slug = slugify('ProductName' + str(i)),
            category = Category.objects.get(name = 'CayegoryName'))
    
    def test_queryset_exists(self):
        qs = Product.objects.all()
        self.assertTrue(qs.exists())
    
    def test_queryset_count(self):
        qs = Product.objects.all()
        self.assertEqual(qs.count(), self.products_count)

    def test_remove(self):
        Product.objects.filter(id=5).delete()
        qs = Product.objects.all()
        self.assertEqual(qs.count(), self.products_count - 1)
