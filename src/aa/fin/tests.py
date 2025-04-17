from django.test import TestCase

from .models import Brand, Spend


class ModelTest(TestCase):
    def setUp(self):
        brand1 = Brand.objects.create(name='Amazon', monthly_budget=3000, daily_budget=200)
        brand2 = Brand.objects.create(name='Bakai', monthly_budget=100, daily_budget=10)
        brand3 = Brand.objects.create(name='Noname', monthly_budget=0, daily_budget=1)
        for x in range(9):
            Spend.objects.create(brand=brand1, amount=1)
            Spend.objects.create(brand=brand2, amount=1)
            Spend.objects.create(brand=brand3, amount=1)

    def test_brand_creation(self):
        brands = Brand.objects
        self.assertEqual(brands.count(), 3)
        self.assertEqual(brands.filter(daily_budget__gt=5).count(), 2)
        self.assertEqual(brands.filter(monthly_budget__lt=5).count(), 1)

    def test_spend_creation(self):
        spends = Spend.objects
        self.assertEqual(spends.count(), 27)
        self.assertEqual(spends.filter(brand__name='Amazon').count(), 9)
