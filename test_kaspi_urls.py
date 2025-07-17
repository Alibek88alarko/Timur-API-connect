#!/usr/bin/env python3
"""
Улучшенный тест с retry механизмом и альтернативными URL
"""
import requests
import time
import os
from dotenv import load_dotenv

load_dotenv()

def test_kaspi_with_alternatives():
    """Тест Kaspi API с альтернативными URL"""
    print("🔍 Тестирование Kaspi API с разными URL...")
    
    token = os.getenv('KASPI_TOKEN')
    headers = {
        'Content-Type': 'application/vnd.api+json',
        'X-Auth-Token': token
    }
    
    # Альтернативные URL для тестирования
    urls_to_test = [
        "https://kaspi.kz/shop/api/v2/orders",
        "https://merchant.kaspi.kz/api/v2/orders", 
        "https://api.kaspi.kz/shop/v2/orders",
        "https://kaspi.kz/merchantapi/v1/orders"
    ]
    
    params = {
        'page[number]': 0,
        'page[size]': 5
    }
    
    for i, url in enumerate(urls_to_test, 1):
        print(f"\n{i}. Тестирование: {url}")
        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)
            print(f"   ✅ Статус: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                orders = data.get('data', [])
                print(f"   📋 Найдено заказов: {len(orders)}")
                print(f"   🎉 РАБОЧИЙ URL: {url}")
                return url
            elif response.status_code == 401:
                print(f"   🔐 Ошибка авторизации - проверьте токен")
            elif response.status_code == 403:
                print(f"   🚫 Доступ запрещен - проверьте права")
            else:
                print(f"   ❌ Ошибка: {response.text[:100]}...")
                
        except requests.exceptions.Timeout:
            print(f"   ⏰ Timeout")
        except requests.exceptions.ConnectionError:
            print(f"   🔌 Ошибка подключения")
        except Exception as e:
            print(f"   ❌ Ошибка: {e}")
    
    return None

def main():
    print("🚀 Улучшенный тест Kaspi API")
    print("=" * 50)
    
    token = os.getenv('KASPI_TOKEN')
    if not token:
        print("❌ KASPI_TOKEN не найден в .env")
        return
    
    print(f"🔑 Используется токен: {token[:10]}...")
    
    working_url = test_kaspi_with_alternatives()
    
    if working_url:
        print(f"\n🎯 Рекомендация: Обновите KASPI_API_URL в .env:")
        print(f"KASPI_API_URL={working_url.replace('/orders', '')}")
    else:
        print("\n❌ Ни один URL не работает")
        print("🔧 Рекомендации:")
        print("   1. Проверьте токен в личном кабинете Kaspi")
        print("   2. Убедитесь, что API включен в настройках")
        print("   3. Обратитесь в техподдержку Kaspi: 2323")

if __name__ == "__main__":
    main()
