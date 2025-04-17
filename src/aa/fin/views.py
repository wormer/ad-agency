import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from aa.fin.models import Brand, Spend


@csrf_exempt
def brand_details(request, brand_id):
    brand = get_object_or_404(Brand, id=brand_id)
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        if name:
            brand.name = name
        monthly_budget = data.get('monthly_budget')
        if monthly_budget:
            brand.monthly_budget = monthly_budget
        daily_budget = data.get('daily_budget')
        if daily_budget:
            brand.daily_budget = daily_budget
        brand.save()
        return JsonResponse({})
    return JsonResponse({
        'name': brand.name,
        'monthly_budget': brand.monthly_budget,
        'daily_budget': brand.daily_budget,
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
