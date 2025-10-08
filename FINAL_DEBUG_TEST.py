#!/usr/bin/env python3
"""
ФИНАЛЬНЫЙ ПРАВИЛЬНЫЙ ТЕСТ с отладкой
"""
import requests
import os
import time
from dotenv import load_dotenv
from urllib.parse import urlencode

load_dotenv()

KASPI_TOKEN = os.getenv('KASPI_TOKEN')

print("=" * 80)
print("🔬 ФИНАЛЬНЫЙ ТЕСТ С ОТЛАДКОЙ")
print("=" * 80)

# User-Agent обязателен!
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'X-Auth-Token': KASPI_TOKEN,
    'Content-Type': 'application/vnd.api+json',
    'Accept': 'application/vnd.api+json'
}

# Дата: последние 14 дней (максимум!)
timestamp_now = int(time.time() * 1000)
timestamp_14_days_ago = timestamp_now - (14 * 24 * 60 * 60 * 1000)

# Параметры
params = {
    'page[number]': '0',
    'page[size]': '20',
    'filter[orders][creationDate][$ge]': str(timestamp_14_days_ago),
    'filter[orders][creationDate][$le]': str(timestamp_now)
}

print(f"\n🔑 Токен: {KASPI_TOKEN[:30]}...")
print(f"\n📅 Период: последние 14 дней")
print(f"   От (timestamp): {timestamp_14_days_ago}")
print(f"   До (timestamp): {timestamp_now}")

print(f"\n📋 Параметры:")
for key, value in params.items():
    print(f"   {key} = {value}")

# Формируем URL вручную для проверки
base_url = "https://kaspi.kz/shop/api/v2/orders"
query_string = urlencode(params)
full_url = f"{base_url}?{query_string}"

print(f"\n🌐 Полный URL:")
print(f"   {full_url[:150]}...")

print(f"\n📡 Отправляю запрос...\n")

try:
    response = requests.get(
        base_url,
        headers=headers,
        params=params,
        timeout=20
    )
    
    status = response.status_code
    
    print("=" * 80)
    print(f"📊 РЕЗУЛЬТАТ: HTTP {status}")
    print("=" * 80)
    
    if status == 200:
        print("\n🎉🎉🎉 УСПЕХ!!! 🎉🎉🎉\n")
        
        data = response.json()
        meta = data.get('meta', {})
        orders = data.get('data', [])
        
        print(f"📦 Всего заказов: {meta.get('totalCount', 0)}")
        print(f"📄 Страниц: {meta.get('pageCount', 0)}")
        print(f"📋 На этой странице: {len(orders)}\n")
        
        if orders:
            print("📋 ЗАКАЗЫ:\n")
            for i, order in enumerate(orders[:5], 1):
                attrs = order.get('attributes', {})
                print(f"[{i}] Заказ №{attrs.get('code')}")
                print(f"    Сумма: {attrs.get('totalPrice')} ₸")
                print(f"    Статус: {attrs.get('status')}")
                print()
        else:
            print("📭 Заказов за последние 14 дней нет\n")
        
        print("=" * 80)
        print("✅ ВСЁ РАБОТАЕТ ИДЕАЛЬНО!")
        print("=" * 80)
        
    elif status == 400:
        print("\n⚠️ HTTP 400\n")
        try:
            error = response.json()
            print("📄 Ошибка от сервера:")
            if 'errors' in error:
                for err in error['errors']:
                    print(f"   • {err.get('title', err)}")
            else:
                print(f"   {error}")
        except:
            print(f"   {response.text[:500]}")
            
    elif status == 401:
        print("\n🔐 HTTP 401 - Неверный токен\n")
        
    else:
        print(f"\n⚠️ Код {status}\n")
        print(response.text[:500])

except requests.Timeout:
    print("\n⏰ TIMEOUT - сервер не ответил за 20 секунд\n")
    print("💡 Проверьте:")
    print("   • User-Agent в заголовках")
    print("   • Firewall/Антивирус")
    
except Exception as e:
    print(f"\n❌ ОШИБКА: {type(e).__name__}")
    print(f"   {str(e)[:300]}\n")

print("=" * 80)
