#!/usr/bin/env python3
"""
Тестирование конфигурации и доступности API
"""
import os
import sys
from dotenv import load_dotenv
import requests

# Загружаем .env
print("=" * 60)
print("🔍 ПРОВЕРКА КОНФИГУРАЦИИ И API")
print("=" * 60)

# Проверяем загрузку .env
env_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(env_path):
    print(f"✅ Файл .env найден: {env_path}")
    load_dotenv(env_path)
else:
    print(f"❌ Файл .env НЕ найден: {env_path}")
    sys.exit(1)

# Проверяем переменные окружения
print("\n" + "=" * 60)
print("📋 ПРОВЕРКА ПЕРЕМЕННЫХ ОКРУЖЕНИЯ")
print("=" * 60)

al_style_token = os.getenv('AL_STYLE_TOKEN')
kaspi_token = os.getenv('KASPI_TOKEN')
al_style_url = os.getenv('AL_STYLE_API_URL')
kaspi_url = os.getenv('KASPI_API_URL')
store_id = os.getenv('STORE_ID')
merchant_id = os.getenv('MERCHANT_ID')
company_name = os.getenv('COMPANY_NAME')

print(f"AL_STYLE_TOKEN: {'✅ Загружен' if al_style_token else '❌ Отсутствует'}")
if al_style_token:
    print(f"  Длина: {len(al_style_token)} символов")
    print(f"  Первые 10 символов: {al_style_token[:10]}...")

print(f"\nKASPI_TOKEN: {'✅ Загружен' if kaspi_token else '❌ Отсутствует'}")
if kaspi_token:
    print(f"  Длина: {len(kaspi_token)} символов")
    print(f"  Первые 10 символов: {kaspi_token[:10]}...")

print(f"\nAL_STYLE_API_URL: {al_style_url}")
print(f"KASPI_API_URL: {kaspi_url}")
print(f"STORE_ID: {store_id}")
print(f"MERCHANT_ID: {merchant_id}")
print(f"COMPANY_NAME: {company_name}")

# Тестируем Al-Style API
print("\n" + "=" * 60)
print("🔍 ТЕСТИРОВАНИЕ AL-STYLE API")
print("=" * 60)

try:
    al_style_test_url = f"{al_style_url}/elements-pagination"
    params = {
        'access-token': al_style_token,
        'limit': 5,
        'offset': 0
    }
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    print(f"📡 Запрос к: {al_style_test_url}")
    response = requests.get(al_style_test_url, headers=headers, params=params, timeout=10)
    
    print(f"📊 Статус: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        products = data.get('elements', [])
        print(f"✅ Al-Style API работает!")
        print(f"📦 Получено товаров: {len(products)}")
        if len(products) > 0:
            print(f"📝 Пример товара: {products[0].get('name', 'N/A')}")
    else:
        print(f"⚠️ Неожиданный статус: {response.status_code}")
        print(f"Ответ: {response.text[:200]}")
        
except requests.exceptions.Timeout:
    print("❌ Timeout при подключении к Al-Style API")
except Exception as e:
    print(f"❌ Ошибка: {e}")

# Тестируем Kaspi API (несколько URL)
print("\n" + "=" * 60)
print("🔍 ТЕСТИРОВАНИЕ KASPI API")
print("=" * 60)

kaspi_urls_to_test = [
    ("Основной", os.getenv('KASPI_API_URL')),
    ("Альтернатива 1", os.getenv('KASPI_API_URL_ALT1')),
    ("Альтернатива 2", os.getenv('KASPI_API_URL_ALT2')),
]

kaspi_headers = {
    'Content-Type': 'application/vnd.api+json',
    'X-Auth-Token': kaspi_token
}

working_kaspi_url = None

for url_name, base_url in kaspi_urls_to_test:
    if not base_url:
        continue
        
    print(f"\n🔗 Тестирую {url_name}: {base_url}")
    
    # Тестируем разные endpoints
    endpoints_to_test = [
        '/orders',
        '/products',
        '/merchants',
        ''  # Базовый URL
    ]
    
    for endpoint in endpoints_to_test:
        test_url = f"{base_url}{endpoint}"
        try:
            print(f"  📡 {test_url}... ", end='')
            response = requests.get(
                test_url,
                headers=kaspi_headers,
                timeout=5,
                params={'page[size]': 1}  # Минимальный запрос
            )
            
            print(f"HTTP {response.status_code}")
            
            if response.status_code in [200, 201, 400, 401, 403]:
                # Даже ошибки авторизации - это хороший знак!
                if response.status_code == 200:
                    print(f"    ✅ РАБОТАЕТ! Этот URL доступен!")
                    working_kaspi_url = base_url
                    break
                elif response.status_code == 401:
                    print(f"    ⚠️ 401 Unauthorized - возможно неверный токен или endpoint")
                elif response.status_code == 403:
                    print(f"    ⚠️ 403 Forbidden - доступ запрещен")
                elif response.status_code == 400:
                    print(f"    ⚠️ 400 Bad Request - возможно неверный формат запроса")
            else:
                print(f"    ⚠️ Неожиданный статус: {response.status_code}")
                
        except requests.exceptions.Timeout:
            print("⏰ Timeout")
        except requests.exceptions.ConnectionError:
            print("❌ Connection Error")
        except Exception as e:
            print(f"❌ Ошибка: {type(e).__name__}")
    
    if working_kaspi_url:
        break

# Итоговый отчет
print("\n" + "=" * 60)
print("📊 ИТОГОВЫЙ ОТЧЕТ")
print("=" * 60)

print("\n✅ РАБОТАЕТ:")
if al_style_token and kaspi_token:
    print("  - Конфигурация загружена (.env файл)")
    print("  - Токены найдены")

print("\n⚠️ ТРЕБУЕТ ВНИМАНИЯ:")
if not working_kaspi_url:
    print("  - Kaspi API недоступен на всех проверенных URL")
    print("  - Возможные причины:")
    print("    1. Неверный токен")
    print("    2. API не активирован в личном кабинете")
    print("    3. Неправильный URL endpoint")
    print("    4. Ограничения доступа по IP")
    print("\n💡 РЕКОМЕНДАЦИИ:")
    print("  1. Проверьте токен в личном кабинете Kaspi.kz")
    print("  2. Убедитесь, что API активирован")
    print("  3. Свяжитесь с техподдержкой Kaspi: 2323")

print("\n" + "=" * 60)
