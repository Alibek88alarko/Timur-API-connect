#!/usr/bin/env python3
"""
Быстрый тест API подключений без блокировки
"""
import requests
import json
import os
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

def test_al_style_api():
    """Быстрый тест Al-Style API"""
    print("🔍 Тестирование Al-Style API...")
    
    url = "https://api.al-style.kz/api/elements-pagination"
    token = os.getenv('AL_STYLE_TOKEN')
    
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    params = {
        'access-token': token,
        'limit': 5,
        'offset': 0
    }
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        print(f"✅ Al-Style API: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            products = data.get('elements', [])
            print(f"📦 Найдено товаров: {len(products)}")
            return True
        else:
            print(f"❌ Ошибка: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("⏰ Timeout при подключении к Al-Style API")
        return False
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

def test_kaspi_api():
    """Быстрый тест Kaspi API"""
    print("\n🔍 Тестирование Kaspi API...")
    
    url = "https://kaspi.kz/shop/api/v2/orders"
    token = os.getenv('KASPI_TOKEN')
    
    headers = {
        'Content-Type': 'application/vnd.api+json',
        'X-Auth-Token': token
    }
    
    params = {
        'page[number]': 0,
        'page[size]': 5
    }
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        print(f"✅ Kaspi API: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            orders = data.get('data', [])
            print(f"📋 Найдено заказов: {len(orders)}")
            return True
        else:
            print(f"❌ Ошибка: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("⏰ Timeout при подключении к Kaspi API")
        return False
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

def main():
    print("🚀 Быстрый тест API подключений")
    print("=" * 40)
    
    # Проверяем токены
    al_token = os.getenv('AL_STYLE_TOKEN')
    kaspi_token = os.getenv('KASPI_TOKEN')
    
    if not al_token:
        print("❌ AL_STYLE_TOKEN не найден")
        return
    
    if not kaspi_token:
        print("❌ KASPI_TOKEN не найден")
        return
    
    print(f"🔑 Al-Style Token: {al_token[:10]}...")
    print(f"🔑 Kaspi Token: {kaspi_token[:10]}...")
    
    # Тестируем API
    al_ok = test_al_style_api()
    kaspi_ok = test_kaspi_api()
    
    print("\n📊 Результаты:")
    print(f"Al-Style API: {'✅ Работает' if al_ok else '❌ Не работает'}")
    print(f"Kaspi API: {'✅ Работает' if kaspi_ok else '❌ Не работает'}")
    
    if al_ok and kaspi_ok:
        print("\n🎉 Оба API работают корректно!")
    else:
        print("\n⚠️  Нужна доработка API подключений")

if __name__ == "__main__":
    main()
