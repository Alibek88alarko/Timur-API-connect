#!/usr/bin/env python3
"""
Быстрый тест токена Kaspi - только проверка доступности
"""
import requests
import os
from dotenv import load_dotenv

load_dotenv()

print("=" * 60)
print("⚡ БЫСТРЫЙ ТЕСТ ТОКЕНА KASPI")
print("=" * 60)

KASPI_TOKEN = os.getenv('KASPI_TOKEN')
print(f"\n🔑 Токен: {KASPI_TOKEN[:20]}..." if KASPI_TOKEN else "❌ Токен не найден")

# Правильные заголовки
HEADERS = {
    'Content-Type': 'application/vnd.api+json',
    'X-Auth-Token': KASPI_TOKEN
}

# Тестируем самый простой endpoint
url = "https://kaspi.kz/shop/api/v2/orders"
params = {'page[number]': 0, 'page[size]': 1}

print(f"\n📡 Тестирую: {url}")
print("⏳ Ожидание ответа (timeout 10 сек)...")

try:
    response = requests.get(url, headers=HEADERS, params=params, timeout=10)
    
    print(f"\n✅ Ответ получен!")
    print(f"📊 HTTP Статус: {response.status_code}")
    
    if response.status_code == 200:
        print("\n🎉 УСПЕХ! ТОКЕН РАБОТАЕТ!")
        try:
            data = response.json()
            if 'data' in data:
                print(f"📦 Данные получены: {len(data['data'])} элементов")
        except:
            pass
        print("\n✅ ТОКЕН КОРРЕКТЕН И АКТИВЕН")
        
    elif response.status_code == 401:
        print("\n❌ 401 UNAUTHORIZED")
        print("🔐 Токен неверный или истёк")
        print("\n📋 ЧТО ДЕЛАТЬ:")
        print("   1. Зайти: https://kaspi.kz/merchantcabinet/")
        print("   2. Настройки → API")
        print("   3. Получить новый токен")
        print("   4. Обновить в .env файле")
        
    elif response.status_code == 403:
        print("\n❌ 403 FORBIDDEN")
        print("🚫 API не активирован для вашего аккаунта")
        print("\n📋 ЧТО ДЕЛАТЬ:")
        print("   1. Зайти в кабинет продавца")
        print("   2. Активировать API")
        print("   3. Или позвонить: 2323")
        
    elif response.status_code == 404:
        print("\n❌ 404 NOT FOUND")
        print("🔍 Endpoint не найден")
        print("   (Это странно, URL должен быть правильным)")
        
    else:
        print(f"\n⚠️ Неожиданный статус: {response.status_code}")
        print(f"📄 Ответ: {response.text[:200]}")
        
except requests.exceptions.Timeout:
    print("\n⏰ TIMEOUT!")
    print("❌ Сервер не отвечает")
    print("\n💡 ВОЗМОЖНЫЕ ПРИЧИНЫ:")
    print("   1. Неверный токен (сервер игнорирует запрос)")
    print("   2. API не активирован")
    print("   3. Проблемы с сетью")
    print("   4. Блокировка firewall")
    print("\n📋 ЧТО ДЕЛАТЬ:")
    print("   1. Проверить токен в кабинете")
    print("   2. Убедиться, что API включен")
    print("   3. Позвонить: 2323")
    
except requests.exceptions.ConnectionError:
    print("\n❌ CONNECTION ERROR")
    print("🌐 Не удалось подключиться к kaspi.kz")
    print("\n💡 ПРОВЕРЬТЕ:")
    print("   - Интернет подключение")
    print("   - Доступ к kaspi.kz")
    
except Exception as e:
    print(f"\n❌ ОШИБКА: {type(e).__name__}")
    print(f"   {str(e)[:100]}")

print("\n" + "=" * 60)
