from django.test import TestCase
from django.urls import reverse

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


class ViewTest(TestCase):
    def setUp(self):
        brand1 = Brand.objects.create(name='Amazon', monthly_budget=3000, daily_budget=200)
        brand2 = Brand.objects.create(name='Bakai', monthly_budget=100, daily_budget=10)
        brand3 = Brand.objects.create(name='Noname', monthly_budget=0, daily_budget=1)
        for x in range(9):
            Spend.objects.create(brand=brand1, amount=1)
            Spend.objects.create(brand=brand2, amount=1)
            Spend.objects.create(brand=brand3, amount=1)

    def test_check_brands(self):
        response = self.client.get(reverse('brand_details', args=[1]))
        data = response.json()
        self.assertEqual(data['name'], 'Amazon')
        self.assertEqual(data['monthly_budget'], '3000.00')
        self.assertEqual(data['daily_budget'], '200.00')
        response = self.client.get(reverse('brand_details', args=[2]))
        data = response.json()
        self.assertEqual(data['name'], 'Bakai')
        self.assertEqual(data['monthly_budget'], '100.00')
        self.assertEqual(data['daily_budget'], '10.00')
        response = self.client.get(reverse('brand_details', args=[3]))
        data = response.json()
        self.assertEqual(data['name'], 'Noname')
        self.assertEqual(data['monthly_budget'], '0.00')
        self.assertEqual(data['daily_budget'], '1.00')

    def test_update_brands(self):
        post_data = {
            'monthly_budget': 3500,
            'daily_budget': 300,
        }
        self.client.post(reverse('brand_details', args=[1]), data=post_data, content_type='application/json')
        response = self.client.get(reverse('brand_details', args=[1]))
        data = response.json()
        self.assertEqual(data['monthly_budget'], '3500.00')
        self.assertEqual(data['daily_budget'], '300.00')

    def test_campaign_status(self):
        response = self.client.get(reverse('campaign_status', args=[1]))
        data = response.json()
        self.assertEqual(data['spends_this_month'], '9.00')
        self.assertEqual(data['spends_today'], '9.00')
        self.assertEqual(data['is_active'], True)
        response = self.client.get(reverse('campaign_status', args=[2]))
        data = response.json()
        self.assertEqual(data['spends_this_month'], '9.00')
        self.assertEqual(data['spends_today'], '9.00')
        self.assertEqual(data['is_active'], True)
        response = self.client.get(reverse('campaign_status', args=[3]))
        data = response.json()
        self.assertEqual(data['spends_this_month'], '9.00')
        self.assertEqual(data['spends_today'], '9.00')
        self.assertEqual(data['is_active'], False)

    def test_register_spend(self):
        response = self.client.get(reverse('campaign_status', args=[2]))
        data = response.json()
        self.assertEqual(data['spends_today'], '9.00')
        self.assertEqual(data['spends_this_month'], '9.00')
        self.assertEqual(data['is_active'], True)
        post_data = {
            'amount': 1.0,
        }
        self.client.post(reverse('register_spends', args=[2]), data=post_data, content_type='application/json')
        response = self.client.get(reverse('campaign_status', args=[2]))
        data = response.json()
        self.assertEqual(data['spends_today'], '10.00')
        self.assertEqual(data['spends_this_month'], '10.00')
        self.assertEqual(data['is_active'], False)
