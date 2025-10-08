#!/usr/bin/env python3
"""
ТЕСТ С ОБЯЗАТЕЛЬНЫМИ ПАРАМЕТРАМИ из документации Kaspi
"""
import requests
import os
from dotenv import load_dotenv

load_dotenv()

KASPI_TOKEN = os.getenv('KASPI_TOKEN')

print("=" * 80)
print("🎯 ТЕСТ С ОБЯЗАТЕЛЬНЫМИ ПАРАМЕТРАМИ ИЗ ДОКУМЕНТАЦИИ")
print("=" * 80)
print(f"\n🔑 Токен: {KASPI_TOKEN[:30]}...")

# ИЗ ДОКУМЕНТАЦИИ - ПРАВИЛЬНЫЙ ФОРМАТ!
headers = {
    'Content-Type': 'application/vnd.api+json',
    'X-Auth-Token': KASPI_TOKEN
}

# ОБЯЗАТЕЛЬНЫЕ параметры из документации
params = {
    'page[number]': 0,  # ОБЯЗАТЕЛЬНО!
    'page[size]': 20    # ОБЯЗАТЕЛЬНО!
}

url = "https://kaspi.kz/shop/api/v2/orders"

print(f"\n📡 URL: {url}")
print(f"📋 Headers: {headers}")
print(f"📋 Params: {params}")

try:
    print("\n⏳ Отправляю запрос...")
    response = requests.get(url, headers=headers, params=params, timeout=15)
    
    status = response.status_code
    print(f"\n✅ HTTP {status}")
    
    if status == 200:
        print("\n🎉🎉🎉 РАБОТАЕТ! ТОКЕН ПРАВИЛЬНЫЙ!")
        try:
            data = response.json()
            print(f"\n📦 Получено заказов: {data.get('meta', {}).get('totalCount', 'N/A')}")
            print(f"📄 Данные: {str(data)[:500]}...")
        except:
            print(f"📄 Ответ: {response.text[:500]}")
    
    elif status == 400:
        print("\n⚠️ HTTP 400 - Bad Request")
        print("Проблема в формате запроса")
        try:
            error = response.json()
            print(f"📄 Ошибка: {error}")
        except:
            print(f"📄 Текст: {response.text[:500]}")
    
    elif status == 401:
        print("\n🔐 HTTP 401 - Unauthorized")
        print("Токен неверный или истёк")
        print(f"📄 Ответ: {response.text[:500]}")
    
    elif status == 403:
        print("\n🚫 HTTP 403 - Forbidden")
        print("Нет прав доступа к API")
        print(f"📄 Ответ: {response.text[:500]}")
    
    else:
        print(f"\n⚠️ Неожиданный статус: {status}")
        print(f"📄 Ответ: {response.text[:500]}")

except requests.Timeout:
    print("\n⏰ TIMEOUT - сервер не ответил за 15 секунд")
    print("\n💡 Это всё ещё означает проблему с токеном/активацией API")

except Exception as e:
    print(f"\n❌ Ошибка: {type(e).__name__}")
    print(f"📄 Детали: {str(e)[:500]}")

print("\n" + "=" * 80)
print("💡 ВАЖНО:")
print("=" * 80)
print("""
Согласно документации Kaspi:
- page[number] - ОБЯЗАТЕЛЬНЫЙ параметр
- page[size] - ОБЯЗАТЕЛЬНЫЙ параметр (максимум 100)

Без этих параметров API возвращает 400 Bad Request!
""")
print("=" * 80)
