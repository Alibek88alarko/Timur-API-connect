#!/usr/bin/env python3
"""
Тест токена на РАЗНЫХ endpoint'ах Kaspi
Чтобы понять, для чего токен предназначен
"""
import requests
import os
from dotenv import load_dotenv

load_dotenv()

print("=" * 70)
print("🔍 ПРОВЕРКА ТОКЕНА НА РАЗНЫХ ENDPOINT'АХ")
print("=" * 70)

KASPI_TOKEN = os.getenv('KASPI_TOKEN')
print(f"\n🔑 Токен: {KASPI_TOKEN[:25]}..." if KASPI_TOKEN else "❌ Токен не найден")

# Правильные заголовки
HEADERS = {
    'Content-Type': 'application/vnd.api+json',
    'X-Auth-Token': KASPI_TOKEN
}

# Альтернативные заголовки (может токен для другого формата?)
HEADERS_ALT1 = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {KASPI_TOKEN}'
}

HEADERS_ALT2 = {
    'Content-Type': 'application/json',
    'X-Auth-Token': KASPI_TOKEN
}

HEADERS_ALT3 = {
    'Authorization': f'Token {KASPI_TOKEN}'
}

# Список endpoint'ов для тестирования
ENDPOINTS = [
    {
        "name": "Orders API (основной)",
        "url": "https://kaspi.kz/shop/api/v2/orders",
        "headers": HEADERS,
        "params": {"page[size]": 1}
    },
    {
        "name": "Orders API (без параметров)",
        "url": "https://kaspi.kz/shop/api/v2/orders",
        "headers": HEADERS,
        "params": {}
    },
    {
        "name": "Products API",
        "url": "https://kaspi.kz/shop/api/v2/products",
        "headers": HEADERS,
        "params": {"page[size]": 1}
    },
    {
        "name": "Merchant API (альтернатива)",
        "url": "https://merchant.kaspi.kz/api/v2/orders",
        "headers": HEADERS,
        "params": {"page[size]": 1}
    },
    {
        "name": "API без /shop",
        "url": "https://kaspi.kz/api/v2/orders",
        "headers": HEADERS,
        "params": {"page[size]": 1}
    },
    {
        "name": "Orders с Bearer token",
        "url": "https://kaspi.kz/shop/api/v2/orders",
        "headers": HEADERS_ALT1,
        "params": {"page[size]": 1}
    },
    {
        "name": "Orders с JSON content-type",
        "url": "https://kaspi.kz/shop/api/v2/orders",
        "headers": HEADERS_ALT2,
        "params": {"page[size]": 1}
    },
    {
        "name": "Orders с Token prefix",
        "url": "https://kaspi.kz/shop/api/v2/orders",
        "headers": HEADERS_ALT3,
        "params": {"page[size]": 1}
    },
]

print("\n" + "=" * 70)
print("📡 ТЕСТИРОВАНИЕ ENDPOINT'ОВ")
print("=" * 70)

success_count = 0
timeout_count = 0
error_count = 0

for i, endpoint in enumerate(ENDPOINTS, 1):
    print(f"\n[{i}/{len(ENDPOINTS)}] {endpoint['name']}")
    print(f"   URL: {endpoint['url']}")
    print(f"   Заголовки: {list(endpoint['headers'].keys())}")
    
    try:
        response = requests.get(
            endpoint['url'],
            headers=endpoint['headers'],
            params=endpoint.get('params', {}),
            timeout=8
        )
        
        status = response.status_code
        print(f"   ✅ Ответ: HTTP {status}")
        
        if status == 200:
            print(f"   🎉 РАБОТАЕТ! Токен подходит для этого endpoint'а!")
            try:
                data = response.json()
                print(f"   📦 Данные: {str(data)[:100]}...")
            except:
                print(f"   📄 Текст: {response.text[:100]}...")
            success_count += 1
            
        elif status == 401:
            print(f"   🔐 401 Unauthorized - токен не подходит")
            error_count += 1
            
        elif status == 403:
            print(f"   🚫 403 Forbidden - нет доступа")
            error_count += 1
            
        elif status == 404:
            print(f"   ❓ 404 Not Found - endpoint не существует")
            error_count += 1
            
        elif status == 400:
            print(f"   ⚠️ 400 Bad Request - неверный формат")
            try:
                err = response.json()
                print(f"   📄 Ошибка: {str(err)[:100]}...")
            except:
                print(f"   📄 Текст: {response.text[:100]}...")
            error_count += 1
            
        else:
            print(f"   ⚠️ Необычный статус: {status}")
            error_count += 1
            
    except requests.exceptions.Timeout:
        print(f"   ⏰ TIMEOUT - сервер не ответил за 8 секунд")
        timeout_count += 1
        
    except requests.exceptions.ConnectionError:
        print(f"   ❌ CONNECTION ERROR - не удалось подключиться")
        error_count += 1
        
    except Exception as e:
        print(f"   ❌ ОШИБКА: {type(e).__name__}")
        error_count += 1

# Итоги
print("\n" + "=" * 70)
print("📊 РЕЗУЛЬТАТЫ")
print("=" * 70)

print(f"\n✅ Успешных ответов (200): {success_count}")
print(f"⏰ Timeout'ов: {timeout_count}")
print(f"❌ Ошибок (401/403/404/400): {error_count}")

if success_count > 0:
    print("\n🎉 ОТЛИЧНО! Токен работает на некоторых endpoint'ах!")
    print("   Используйте те endpoint'ы, которые вернули 200.")
    
elif timeout_count == len(ENDPOINTS):
    print("\n⚠️ ВСЕ ENDPOINT'Ы ДАЮТ TIMEOUT")
    print("\n💡 ЭТО ЗНАЧИТ:")
    print("   1. Токен вообще не для API (возможно для веб-интерфейса)")
    print("   2. API не активирован")
    print("   3. Неверный токен")
    print("\n📋 ЧТО ДЕЛАТЬ:")
    print("   1. Проверьте в кабинете продавца: Настройки → API")
    print("   2. Убедитесь, что берёте токен именно для API")
    print("   3. Позвоните: 2323")
    
elif error_count > 0:
    print("\n⚠️ ТОКЕН НЕ РАБОТАЕТ НА ЭТИХ ENDPOINT'АХ")
    print("\n💡 ВОЗМОЖНЫЕ ПРИЧИНЫ:")
    print("   1. Токен для другого сервиса Kaspi (не для магазина)")
    print("   2. Токен истёк")
    print("   3. Неверные права доступа")
    print("\n📋 ЧТО ДЕЛАТЬ:")
    print("   1. Проверьте, что токен для 'Магазина на Kaspi.kz'")
    print("   2. Не путайте с токенами для:")
    print("      - Kaspi Pay")
    print("      - Kaspi QR")
    print("      - Kaspi Объявления")
    print("   3. Получите новый токен в разделе API")

print("\n" + "=" * 70)
print("💡 СОВЕТ:")
print("=" * 70)
print("""
В кабинете продавца (https://kaspi.kz/merchantcabinet/) могут быть
РАЗНЫЕ токены для РАЗНЫХ сервисов:

1. Токен для Магазина (Shop API) - для заказов и товаров
2. Токен для Kaspi Pay - для платежей
3. Токен для загрузки товаров (XML API) - для прайс-листов

Убедитесь, что используете токен ИМЕННО для Shop API!
""")
print("=" * 70)
