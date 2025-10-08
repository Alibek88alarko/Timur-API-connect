#!/usr/bin/env python3
"""
БЫСТРАЯ проверка токена - только критичные endpoint'ы
"""
import requests
import os
from dotenv import load_dotenv

load_dotenv()

KASPI_TOKEN = os.getenv('KASPI_TOKEN')
print("=" * 70)
print("⚡ БЫСТРАЯ ПРОВЕРКА ТОКЕНА")
print("=" * 70)
print(f"\n🔑 Токен: {KASPI_TOKEN[:25]}..." if KASPI_TOKEN else "❌ Токен не найден")

# Критичные endpoint'ы с коротким timeout
TESTS = [
    {
        "name": "XML Upload API (POST)",
        "method": "POST",
        "url": "https://kaspi.kz/shop/api/v2/product/import",
        "headers": {
            'Content-Type': 'application/xml',
            'X-Auth-Token': KASPI_TOKEN
        },
        "data": '<?xml version="1.0" encoding="UTF-8"?><root></root>'
    },
    {
        "name": "Products GET",
        "method": "GET",
        "url": "https://kaspi.kz/shop/api/v2/products",
        "headers": {
            'X-Auth-Token': KASPI_TOKEN
        },
        "data": None
    },
    {
        "name": "API Root",
        "method": "GET",
        "url": "https://kaspi.kz/shop/api",
        "headers": {
            'X-Auth-Token': KASPI_TOKEN
        },
        "data": None
    },
    {
        "name": "Merchant API",
        "method": "GET",
        "url": "https://merchant.kaspi.kz/api/v2/orders",
        "headers": {
            'X-Auth-Token': KASPI_TOKEN
        },
        "data": None
    }
]

print("\n" + "=" * 70)

for i, test in enumerate(TESTS, 1):
    print(f"\n[{i}/{len(TESTS)}] {test['name']}")
    print(f"   {test['method']} {test['url']}")
    
    try:
        if test['method'] == 'POST':
            response = requests.post(
                test['url'],
                headers=test['headers'],
                data=test['data'],
                timeout=5
            )
        else:
            response = requests.get(
                test['url'],
                headers=test['headers'],
                timeout=5
            )
        
        status = response.status_code
        print(f"   ✅ HTTP {status}")
        
        if status == 200:
            print(f"   🎉 РАБОТАЕТ!")
            print(f"   📄 Ответ: {response.text[:200]}")
        elif status == 401:
            print(f"   🔐 401 - Неверный токен")
        elif status == 403:
            print(f"   🚫 403 - Нет доступа")
        elif status == 400:
            print(f"   ⚠️ 400 - Неверный запрос")
            print(f"   📄 {response.text[:200]}")
        elif status == 404:
            print(f"   ❓ 404 - Endpoint не найден")
        else:
            print(f"   ⚠️ {response.text[:200]}")
            
    except requests.exceptions.Timeout:
        print(f"   ⏰ TIMEOUT (5 сек)")
    except requests.exceptions.ConnectionError as e:
        print(f"   ❌ Ошибка соединения")
    except Exception as e:
        print(f"   ❌ {type(e).__name__}: {str(e)[:100]}")

print("\n" + "=" * 70)
print("💡 ВАЖНО:")
print("=" * 70)
print("""
Если ВСЕ endpoint'ы дают TIMEOUT:
→ Токен НЕ для REST API, возможно для веб-интерфейса

Если есть 401/403:
→ Токен для API, но неверный или истёк

Если есть 400:
→ Токен правильный, но неверный формат запроса

Если есть 200:
→ ВСЁ РАБОТАЕТ! 🎉
""")
print("=" * 70)

# Дополнительная проверка: попробуем понять, что это за токен
print("\n🔍 АНАЛИЗ ТОКЕНА:")
print(f"   Длина: {len(KASPI_TOKEN)} символов")
print(f"   Формат: {'Base64' if KASPI_TOKEN.endswith('=') else 'Обычный'}")

if len(KASPI_TOKEN) == 44 and KASPI_TOKEN.endswith('='):
    print("   ✅ Похож на корректный API токен Kaspi")
else:
    print("   ⚠️ Нестандартная длина для Kaspi API токена")
