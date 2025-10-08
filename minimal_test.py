#!/usr/bin/env python3
"""
МИНИМАЛЬНЫЙ ТЕСТ - Только обязательное из документации
"""
import requests
import os
from dotenv import load_dotenv

load_dotenv()

KASPI_TOKEN = os.getenv('KASPI_TOKEN')

print("=" * 80)
print("🧪 МИНИМАЛЬНЫЙ ТЕСТ KASPI API")
print("=" * 80)

# Вариант 1: Абсолютный минимум
print("\n[1/5] Абсолютный минимум - только токен и page параметры")
try:
    response = requests.get(
        'https://kaspi.kz/shop/api/v2/orders',
        headers={'X-Auth-Token': KASPI_TOKEN},
        params={'page[number]': '0', 'page[size]': '20'},
        timeout=10
    )
    print(f"   ✅ HTTP {response.status_code}")
    if response.status_code == 200:
        print(f"   🎉 РАБОТАЕТ!")
        print(f"   📦 {response.json().get('meta', {})}")
except Exception as e:
    print(f"   ❌ {type(e).__name__}")

# Вариант 2: С Content-Type
print("\n[2/5] С Content-Type: application/vnd.api+json")
try:
    response = requests.get(
        'https://kaspi.kz/shop/api/v2/orders',
        headers={
            'X-Auth-Token': KASPI_TOKEN,
            'Content-Type': 'application/vnd.api+json'
        },
        params={'page[number]': '0', 'page[size]': '20'},
        timeout=10
    )
    print(f"   ✅ HTTP {response.status_code}")
    if response.status_code == 200:
        print(f"   🎉 РАБОТАЕТ!")
except Exception as e:
    print(f"   ❌ {type(e).__name__}")

# Вариант 3: С Accept вместо Content-Type
print("\n[3/5] С Accept: application/vnd.api+json")
try:
    response = requests.get(
        'https://kaspi.kz/shop/api/v2/orders',
        headers={
            'X-Auth-Token': KASPI_TOKEN,
            'Accept': 'application/vnd.api+json'
        },
        params={'page[number]': '0', 'page[size]': '20'},
        timeout=10
    )
    print(f"   ✅ HTTP {response.status_code}")
    if response.status_code == 200:
        print(f"   🎉 РАБОТАЕТ!")
except Exception as e:
    print(f"   ❌ {type(e).__name__}")

# Вариант 4: С числовыми параметрами (не строки)
print("\n[4/5] С числовыми параметрами page")
try:
    response = requests.get(
        'https://kaspi.kz/shop/api/v2/orders',
        headers={
            'X-Auth-Token': KASPI_TOKEN,
            'Content-Type': 'application/vnd.api+json'
        },
        params={'page[number]': 0, 'page[size]': 20},  # Числа, не строки
        timeout=10
    )
    print(f"   ✅ HTTP {response.status_code}")
    if response.status_code == 200:
        print(f"   🎉 РАБОТАЕТ!")
except Exception as e:
    print(f"   ❌ {type(e).__name__}")

# Вариант 5: Через URL напрямую (без params)
print("\n[5/5] URL с параметрами напрямую в строке")
try:
    response = requests.get(
        'https://kaspi.kz/shop/api/v2/orders?page%5Bnumber%5D=0&page%5Bsize%5D=20',
        headers={
            'X-Auth-Token': KASPI_TOKEN,
            'Content-Type': 'application/vnd.api+json'
        },
        timeout=10
    )
    print(f"   ✅ HTTP {response.status_code}")
    if response.status_code == 200:
        print(f"   🎉 РАБОТАЕТ!")
        print(f"   📄 {response.text[:200]}")
except Exception as e:
    print(f"   ❌ {type(e).__name__}")

print("\n" + "=" * 80)
