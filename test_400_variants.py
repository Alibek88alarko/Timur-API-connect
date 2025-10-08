#!/usr/bin/env python3
"""
Тест после получения HTTP 400 - ищем правильный формат
"""
import requests
import os
from dotenv import load_dotenv

load_dotenv()

KASPI_TOKEN = os.getenv('KASPI_TOKEN')

print("=" * 80)
print("🎯 ТЕСТ ПОСЛЕ HTTP 400 - ИЩЕМ ПРАВИЛЬНЫЙ ФОРМАТ")
print("=" * 80)

# Пробуем разные варианты
tests = [
    {
        "name": "Без параметров вообще",
        "url": "https://kaspi.kz/shop/api/v2/orders",
        "headers": {"X-Auth-Token": KASPI_TOKEN},
        "params": None
    },
    {
        "name": "С page.size (точка вместо скобок)",
        "url": "https://kaspi.kz/shop/api/v2/orders",
        "headers": {"X-Auth-Token": KASPI_TOKEN},
        "params": {"page.size": "1", "page.number": "0"}
    },
    {
        "name": "С page_size (underscore)",
        "url": "https://kaspi.kz/shop/api/v2/orders",
        "headers": {"X-Auth-Token": KASPI_TOKEN},
        "params": {"page_size": "1", "page_number": "0"}
    },
    {
        "name": "Простые параметры",
        "url": "https://kaspi.kz/shop/api/v2/orders",
        "headers": {"X-Auth-Token": KASPI_TOKEN},
        "params": {"size": "1", "page": "0"}
    },
    {
        "name": "Со стандартным Content-Type",
        "url": "https://kaspi.kz/shop/api/v2/orders",
        "headers": {
            "X-Auth-Token": KASPI_TOKEN,
            "Content-Type": "application/vnd.api+json"
        },
        "params": {"page[size]": "1"}
    },
    {
        "name": "С Accept вместо Content-Type",
        "url": "https://kaspi.kz/shop/api/v2/orders",
        "headers": {
            "X-Auth-Token": KASPI_TOKEN,
            "Accept": "application/vnd.api+json"
        },
        "params": {"page[size]": "1"}
    },
    {
        "name": "Только токен, без параметров",
        "url": "https://kaspi.kz/shop/api/v2/orders",
        "headers": {"X-Auth-Token": KASPI_TOKEN},
        "params": {}
    },
    {
        "name": "Products вместо Orders",
        "url": "https://kaspi.kz/shop/api/v2/products",
        "headers": {"X-Auth-Token": KASPI_TOKEN},
        "params": {}
    },
]

success_found = False

for i, test in enumerate(tests, 1):
    print(f"\n[{i}/{len(tests)}] {test['name']}")
    print(f"   URL: {test['url']}")
    print(f"   Headers: {list(test['headers'].keys())}")
    print(f"   Params: {test['params']}")
    
    try:
        response = requests.get(
            test['url'],
            headers=test['headers'],
            params=test['params'],
            timeout=5
        )
        
        status = response.status_code
        print(f"   ✅ HTTP {status}")
        
        if status == 200:
            print(f"   🎉 РАБОТАЕТ!!!")
            try:
                data = response.json()
                print(f"   📦 JSON: {str(data)[:200]}")
                success_found = True
            except:
                print(f"   📄 Текст: {response.text[:200]}")
                
        elif status == 400:
            print(f"   ⚠️ Bad Request")
            try:
                error = response.json()
                print(f"   📄 Ошибка: {error}")
            except:
                print(f"   📄 Текст: {response.text[:200]}")
                
        elif status == 401:
            print(f"   🔐 Unauthorized - токен неверный")
            
        elif status == 403:
            print(f"   🚫 Forbidden - нет прав")
            
        else:
            print(f"   ℹ️ Ответ: {response.text[:200]}")
            
    except requests.Timeout:
        print(f"   ⏰ TIMEOUT")
    except Exception as e:
        print(f"   ❌ {type(e).__name__}: {str(e)[:100]}")

print("\n" + "=" * 80)
if success_found:
    print("🎉 НАЙДЕН РАБОЧИЙ ВАРИАНТ! Используйте его!")
else:
    print("⚠️ Рабочий вариант не найден")
    print("\n💡 Возможные причины HTTP 400:")
    print("   1. Неверный формат параметров pagination")
    print("   2. Требуются дополнительные заголовки")
    print("   3. Нужен другой endpoint")
    print("   4. API ждёт POST вместо GET")
print("=" * 80)
