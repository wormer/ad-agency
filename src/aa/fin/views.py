import json

from decimal import Decimal

from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from aa.fin.dayparting import dayparting_from_json, dayparting_to_json, is_time_in_dayparting
from aa.fin.models import Brand, Spend



@csrf_exempt
def brand_list(request):
    brands = Brand.objects.all()
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data['name']
        monthly_budget = data['monthly_budget']
        daily_budget = data['daily_budget']
        dayparting = data.get('dayparting', [])
        brand = Brand.objects.create(
            name=name,
            daily_budget=daily_budget,
            monthly_budget=monthly_budget,
            dayparting=dayparting_to_json(dayparting_from_json(dayparting)),
        )
        return JsonResponse({
            'id': brand.id,
        })
    return JsonResponse({
        'brands': [{
            'id': brand.id,
            'name': brand.name,
        } for brand in brands],
    })


@csrf_exempt
def brand_details(request, brand_id):
    brand = get_object_or_404(Brand, id=brand_id)
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        if name:
            brand.name = name
        monthly_budget = data.get('monthly_budget')
        if monthly_budget is not None:
            brand.monthly_budget = monthly_budget
        daily_budget = data.get('daily_budget')
        if daily_budget is not None:
            brand.daily_budget = daily_budget
        dayparting = data.get('dayparting')
        if dayparting is not None and isinstance(dayparting, list):
            brand.dayparting = dayparting_to_json(dayparting_from_json(dayparting))
        brand.save()
        return JsonResponse({})
    return JsonResponse({
        'name': brand.name,
        'monthly_budget': brand.monthly_budget,
        'daily_budget': brand.daily_budget,
        'dayparting': brand.dayparting,
    })


@csrf_exempt
def register_spend(request, brand_id):
    brand = get_object_or_404(Brand, id=brand_id)
    if request.method == 'POST':
        data = json.loads(request.body)
        amount = data.get('amount')
        if amount:
            Spend.objects.create(brand=brand, amount=amount)
    return JsonResponse({})


def campaign_status(request, brand_id):
    brand = get_object_or_404(Brand, id=brand_id)
    now = timezone.now()
    day_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    month_start = day_start.replace(day=1)
    spends = Spend.objects.filter(brand=brand, datetime__lte=now)
    amount_today = round(spends.filter(datetime__gte=day_start).aggregate(sum=Sum('amount'))['sum'] or Decimal(0.0), ndigits=2)
    amount_this_month = round(spends.filter(datetime__gte=month_start).aggregate(sum=Sum('amount'))['sum'] or Decimal(0.0), ndigits=2)
    is_dayparting_respected = is_time_in_dayparting(now.time(), dayparting_from_json(brand.dayparting))
    return JsonResponse({
        'spends_this_month': amount_this_month,
        'spends_today': amount_today,
        'is_active': is_dayparting_respected and amount_this_month < brand.monthly_budget and amount_today < brand.daily_budget,
    })
