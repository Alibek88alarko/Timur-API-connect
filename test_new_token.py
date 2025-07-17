#!/usr/bin/env python3
"""
Тест токена API после генерации в кабинете продавца
"""
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

def test_token_after_generation():
    """Тест нового токена из кабинета продавца"""
    print("🔐 Тест токена API после генерации в кабинете")
    print("=" * 50)
    
    token = os.getenv('KASPI_TOKEN')
    if not token or token == 'your_kaspi_token_here':
        print("❌ Токен не найден или не обновлен в .env")
        print("📋 Инструкция:")
        print("1. Зайдите в кабинет продавца Kaspi.kz")
        print("2. Настройки → Токен API")
        print("3. Нажмите 'Сформировать'")
        print("4. Скопируйте токен в .env файл")
        return False
    
    print(f"🔑 Тестируем токен: {token[:15]}...")
    
    # Тестируем разные endpoints
    endpoints_to_test = [
        ("GET", "/orders", "Получение заказов"),
        ("GET", "/products", "Получение товаров"),
        ("GET", "/warehouses", "Получение складов"),
        ("GET", "/orders?page[size]=1", "Тест с параметрами")
    ]
    
    base_urls = [
        "https://kaspi.kz/shop/api/v2",
        "https://merchant.kaspi.kz/api/v2"
    ]
    
    headers = {
        'Content-Type': 'application/vnd.api+json',
        'X-Auth-Token': token
    }
    
    success_count = 0
    
    for base_url in base_urls:
        print(f"\n🌐 Тестируем базовый URL: {base_url}")
        
        for method, endpoint, description in endpoints_to_test:
            url = f"{base_url}{endpoint}"
            print(f"  📡 {description}: {endpoint}")
            
            try:
                response = requests.request(method, url, headers=headers, timeout=10)
                status = response.status_code
                
                if status == 200:
                    print(f"    ✅ {status} - Успешно!")
                    try:
                        data = response.json()
                        if 'data' in data:
                            print(f"    📊 Найдено записей: {len(data['data'])}")
                        success_count += 1
                    except:
                        print(f"    📄 Ответ получен (не JSON)")
                        
                elif status == 401:
                    print(f"    🔐 {status} - Проблема с авторизацией")
                    print(f"    💡 Проверьте токен в кабинете продавца")
                    
                elif status == 403:
                    print(f"    🚫 {status} - Доступ запрещен")
                    print(f"    💡 Проверьте права доступа к API")
                    
                elif status == 404:
                    print(f"    🔍 {status} - Endpoint не найден")
                    
                elif status == 429:
                    print(f"    ⏰ {status} - Превышен лимит запросов")
                    
                else:
                    print(f"    ❓ {status} - {response.text[:100]}...")
                    
            except requests.exceptions.Timeout:
                print(f"    ⏰ Timeout")
            except requests.exceptions.ConnectionError:
                print(f"    🔌 Ошибка соединения")
            except Exception as e:
                print(f"    ❌ Ошибка: {e}")
    
    print(f"\n📈 Результат: {success_count} успешных запросов")
    
    if success_count > 0:
        print("🎉 Токен работает! API доступен!")
        return True
    else:
        print("❌ API недоступен")
        print("\n🔧 Следующие шаги:")
        print("1. Проверьте активность токена в кабинете")
        print("2. Убедитесь, что API включен")
        print("3. Обратитесь в техподдержку: 2323")
        return False

if __name__ == "__main__":
    test_token_after_generation()
