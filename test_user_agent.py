#!/usr/bin/env python3
"""
Тест с User-Agent браузера
"""
import requests
import os
from dotenv import load_dotenv

load_dotenv()

KASPI_TOKEN = os.getenv('KASPI_TOKEN')

print("🧪 ТЕСТ С USER-AGENT БРАУЗЕРА")
print("=" * 80)

# Эмулируем браузер Chrome
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'X-Auth-Token': KASPI_TOKEN,
    'Content-Type': 'application/vnd.api+json',
    'Accept': 'application/vnd.api+json'
}

params = {
    'page[number]': 0,
    'page[size]': 20
}

print("\n🌐 Тест 1: Главная страница kaspi.kz")
try:
    response = requests.get('https://kaspi.kz', headers={'User-Agent': headers['User-Agent']}, timeout=10)
    print(f"   ✅ HTTP {response.status_code} - Сайт доступен!")
except Exception as e:
    print(f"   ❌ {type(e).__name__} - Сайт недоступен")

print("\n📡 Тест 2: API с User-Agent браузера")
try:
    response = requests.get(
        'https://kaspi.kz/shop/api/v2/orders',
        headers=headers,
        params=params,
        timeout=15
    )
    print(f"   ✅ HTTP {response.status_code}")
    
    if response.status_code == 200:
        print("   🎉🎉🎉 РАБОТАЕТ!!!")
        data = response.json()
        print(f"   📦 Заказов: {data.get('meta', {}).get('totalCount', 0)}")
    elif response.status_code == 400:
        print("   ⚠️ HTTP 400 - но хотя бы ответ есть!")
        print(f"   📄 {response.text[:300]}")
    else:
        print(f"   📄 {response.text[:300]}")
        
except requests.Timeout:
    print("   ⏰ Всё равно Timeout")
except Exception as e:
    print(f"   ❌ {type(e).__name__}: {str(e)[:100]}")

print("\n" + "=" * 80)
