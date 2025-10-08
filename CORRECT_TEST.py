#!/usr/bin/env python3
"""
ПРАВИЛЬНЫЙ ЗАПРОС - С ОБЯЗАТЕЛЬНОЙ ДАТОЙ!
"""
import requests
import os
import time
from dotenv import load_dotenv

load_dotenv()

KASPI_TOKEN = os.getenv('KASPI_TOKEN')

print("=" * 80)
print("🎉 ПРАВИЛЬНЫЙ ЗАПРОС К KASPI API - С ДАТОЙ!")
print("=" * 80)

# User-Agent браузера (без него timeout!)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'X-Auth-Token': KASPI_TOKEN,
    'Content-Type': 'application/vnd.api+json'
}

# Дата: последние 30 дней
timestamp_now = int(time.time() * 1000)
timestamp_30_days_ago = timestamp_now - (30 * 24 * 60 * 60 * 1000)

# ПРАВИЛЬНЫЕ параметры с датой!
params = {
    'page[number]': 0,
    'page[size]': 20,
    'filter[orders][creationDate][$ge]': timestamp_30_days_ago,  # ОБЯЗАТЕЛЬНО!
    'filter[orders][creationDate][$le]': timestamp_now           # ОБЯЗАТЕЛЬНО!
}

print(f"\n🔑 Токен: {KASPI_TOKEN[:30]}...")
print(f"📅 Период: последние 30 дней")
print(f"   От: {timestamp_30_days_ago}")
print(f"   До: {timestamp_now}")

print(f"\n📡 Отправляю запрос...")

try:
    response = requests.get(
        'https://kaspi.kz/shop/api/v2/orders',
        headers=headers,
        params=params,
        timeout=15
    )
    
    status = response.status_code
    
    print("\n" + "=" * 80)
    print(f"📊 РЕЗУЛЬТАТ: HTTP {status}")
    print("=" * 80)
    
    if status == 200:
        print("\n🎉🎉🎉 УСПЕХ!!! API РАБОТАЕТ!!! 🎉🎉🎉")
        
        data = response.json()
        total = data.get('meta', {}).get('totalCount', 0)
        page_count = data.get('meta', {}).get('pageCount', 0)
        orders = data.get('data', [])
        
        print(f"\n📦 СТАТИСТИКА:")
        print(f"   Всего заказов: {total}")
        print(f"   Страниц: {page_count}")
        print(f"   На этой странице: {len(orders)}")
        
        if orders:
            print(f"\n📋 ПЕРВЫЕ 3 ЗАКАЗА:")
            for i, order in enumerate(orders[:3], 1):
                attrs = order.get('attributes', {})
                print(f"\n   [{i}] Заказ #{attrs.get('code')}")
                print(f"       ID: {order.get('id')}")
                print(f"       Сумма: {attrs.get('totalPrice')} ₸")
                print(f"       Статус: {attrs.get('status')}")
                print(f"       Состояние: {attrs.get('state')}")
                customer = attrs.get('customer', {})
                if customer:
                    print(f"       Клиент: {customer.get('firstName')} {customer.get('lastName')}")
        else:
            print("\n📭 Заказов за последние 30 дней нет")
        
        print("\n" + "=" * 80)
        print("✅ ВСЁ РАБОТАЕТ! ИНТЕГРАЦИЯ ГОТОВА!")
        print("=" * 80)
        print("\n📝 Следующие шаги:")
        print("   1. Обновите Script.py с правильными параметрами")
        print("   2. Добавьте User-Agent в config.py")
        print("   3. Не забывайте про обязательные даты!")
        
    elif status == 400:
        print("\n⚠️ HTTP 400 - Bad Request")
        try:
            error = response.json()
            print(f"\n📄 Ошибка:")
            print(f"   {error}")
        except:
            print(f"   {response.text[:500]}")
    
    elif status == 401:
        print("\n🔐 HTTP 401 - Unauthorized")
        print("   Токен неверный")
    
    else:
        print(f"\n⚠️ Неожиданный код: {status}")
        print(f"   {response.text[:500]}")

except requests.Timeout:
    print("\n⏰ TIMEOUT")
    print("   Проверьте User-Agent!")

except Exception as e:
    print(f"\n❌ ОШИБКА: {type(e).__name__}")
    print(f"   {str(e)[:300]}")

print("\n" + "=" * 80)
