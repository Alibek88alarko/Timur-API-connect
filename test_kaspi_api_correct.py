#!/usr/bin/env python3
"""
Тест Kaspi API с правильными endpoint'ами (2025)
На основе официальной документации
"""
import requests
import os
from dotenv import load_dotenv

# Загружаем .env
load_dotenv()

print("=" * 70)
print("🧪 ТЕСТ KASPI API С ПРАВИЛЬНЫМИ ENDPOINT'АМИ")
print("=" * 70)

# Конфигурация
KASPI_TOKEN = os.getenv('KASPI_TOKEN')
BASE_URL = "https://kaspi.kz"

# Правильные заголовки согласно документации
HEADERS = {
    'Content-Type': 'application/vnd.api+json',
    'X-Auth-Token': KASPI_TOKEN
}

print(f"\n🔑 Токен загружен: {KASPI_TOKEN[:15]}..." if KASPI_TOKEN else "❌ Токен не найден!")
print(f"🌐 Базовый URL: {BASE_URL}")

# Список endpoint'ов для тестирования
ENDPOINTS_TO_TEST = [
    {
        "name": "Заказы - Базовый",
        "url": f"{BASE_URL}/shop/api/v2/orders",
        "method": "GET",
        "params": {
            "page[number]": 0,
            "page[size]": 1
        }
    },
    {
        "name": "Заказы - Новые (APPROVED_BY_BANK)",
        "url": f"{BASE_URL}/shop/api/v2/orders",
        "method": "GET",
        "params": {
            "page[number]": 0,
            "page[size]": 5,
            "filter[orders][status]": "APPROVED_BY_BANK"
        }
    },
    {
        "name": "Заказы - Принятые",
        "url": f"{BASE_URL}/shop/api/v2/orders",
        "method": "GET",
        "params": {
            "page[number]": 0,
            "page[size]": 5,
            "filter[orders][status]": "ACCEPTED_BY_MERCHANT"
        }
    },
    {
        "name": "Товары (Products)",
        "url": f"{BASE_URL}/shop/api/v2/products",
        "method": "GET",
        "params": {
            "page[number]": 0,
            "page[size]": 1
        }
    },
]

print("\n" + "=" * 70)
print("📡 ТЕСТИРОВАНИЕ ENDPOINT'ОВ")
print("=" * 70)

success_count = 0
fail_count = 0
working_endpoints = []

for endpoint in ENDPOINTS_TO_TEST:
    print(f"\n🔗 {endpoint['name']}")
    print(f"   URL: {endpoint['url']}")
    print(f"   Метод: {endpoint['method']}")
    
    if endpoint.get('params'):
        print(f"   Параметры: {endpoint['params']}")
    
    try:
        if endpoint['method'] == 'GET':
            response = requests.get(
                endpoint['url'],
                headers=HEADERS,
                params=endpoint.get('params', {}),
                timeout=15
            )
        else:
            response = requests.post(
                endpoint['url'],
                headers=HEADERS,
                json=endpoint.get('body', {}),
                timeout=15
            )
        
        print(f"   📊 Статус: {response.status_code}")
        
        # Анализируем ответ
        if response.status_code == 200:
            print(f"   ✅ УСПЕХ! API работает!")
            try:
                data = response.json()
                if 'data' in data:
                    items_count = len(data['data']) if isinstance(data['data'], list) else 1
                    print(f"   📦 Получено элементов: {items_count}")
                    
                    if items_count > 0:
                        print(f"   📝 Пример данных:")
                        first_item = data['data'][0] if isinstance(data['data'], list) else data['data']
                        if 'type' in first_item:
                            print(f"      - Тип: {first_item['type']}")
                        if 'id' in first_item:
                            print(f"      - ID: {first_item['id']}")
                        if 'attributes' in first_item:
                            attrs = first_item['attributes']
                            if 'code' in attrs:
                                print(f"      - Код: {attrs['code']}")
                            if 'status' in attrs:
                                print(f"      - Статус: {attrs['status']}")
                else:
                    print(f"   📄 Ответ: {str(data)[:100]}...")
            except:
                print(f"   📄 Текст ответа: {response.text[:200]}...")
            
            success_count += 1
            working_endpoints.append(endpoint['name'])
            
        elif response.status_code == 401:
            print(f"   🔐 401 Unauthorized - Проблема с токеном!")
            print(f"      Решение: Проверьте токен в кабинете продавца")
            fail_count += 1
            
        elif response.status_code == 403:
            print(f"   🚫 403 Forbidden - Доступ запрещён!")
            print(f"      Решение: API не активирован или нет прав")
            fail_count += 1
            
        elif response.status_code == 404:
            print(f"   ❓ 404 Not Found - Endpoint не найден!")
            print(f"      Решение: Проверьте правильность URL")
            fail_count += 1
            
        elif response.status_code == 400:
            print(f"   ⚠️ 400 Bad Request - Неверный запрос!")
            try:
                error_data = response.json()
                print(f"      Детали: {error_data}")
            except:
                print(f"      Ответ: {response.text[:200]}")
            fail_count += 1
            
        else:
            print(f"   ⚠️ Неожиданный статус: {response.status_code}")
            print(f"      Ответ: {response.text[:200]}")
            fail_count += 1
            
    except requests.exceptions.Timeout:
        print(f"   ⏰ TIMEOUT - Превышено время ожидания")
        print(f"      Возможные причины:")
        print(f"      - Проблемы с сетью")
        print(f"      - Сервер перегружен")
        print(f"      - Неверный endpoint")
        fail_count += 1
        
    except requests.exceptions.ConnectionError as e:
        print(f"   ❌ CONNECTION ERROR - Ошибка подключения")
        print(f"      Детали: {str(e)[:100]}")
        fail_count += 1
        
    except Exception as e:
        print(f"   ❌ ОШИБКА: {type(e).__name__}")
        print(f"      Детали: {str(e)[:100]}")
        fail_count += 1

# Итоговый отчёт
print("\n" + "=" * 70)
print("📊 ИТОГОВЫЙ ОТЧЁТ")
print("=" * 70)

print(f"\n✅ Успешных запросов: {success_count}")
print(f"❌ Неудачных запросов: {fail_count}")
print(f"📈 Процент успеха: {(success_count / (success_count + fail_count) * 100):.1f}%")

if working_endpoints:
    print(f"\n🎯 РАБОТАЮЩИЕ ENDPOINT'Ы:")
    for ep in working_endpoints:
        print(f"   ✅ {ep}")
else:
    print(f"\n⚠️ НИ ОДИН ENDPOINT НЕ РАБОТАЕТ!")
    print(f"\n💡 ВОЗМОЖНЫЕ ПРИЧИНЫ:")
    print(f"   1. Неверный или истёкший токен")
    print(f"   2. API не активирован в кабинете продавца")
    print(f"   3. Ограничения доступа по IP")
    print(f"   4. Проблемы с сетью/firewall")
    
    print(f"\n🔧 ЧТО ДЕЛАТЬ:")
    print(f"   1. Зайдите в кабинет продавца: https://kaspi.kz/merchantcabinet/")
    print(f"   2. Проверьте раздел: Настройки → API")
    print(f"   3. Убедитесь, что API активирован")
    print(f"   4. Проверьте/обновите токен")
    print(f"   5. Свяжитесь с техподдержкой: 2323")

print("\n" + "=" * 70)
print("📞 ТЕХПОДДЕРЖКА KASPI: 2323 (бесплатно)")
print("=" * 70)
