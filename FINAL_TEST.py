#!/usr/bin/env python3
"""
ФИНАЛЬНЫЙ ТЕСТ - С ПРАВИЛЬНЫМИ ПАРАМЕТРАМИ ИЗ ДОКУМЕНТАЦИИ
"""
import requests
import os
import sys
from dotenv import load_dotenv

load_dotenv()

KASPI_TOKEN = os.getenv('KASPI_TOKEN')

print("=" * 80)
print("🎯 ФИНАЛЬНЫЙ ТЕСТ KASPI API")
print("=" * 80)
print(f"\n📅 Дата: 8 октября 2025")
print(f"🔑 Токен: {KASPI_TOKEN[:30]}..." if KASPI_TOKEN else "❌ Токен не найден")

if not KASPI_TOKEN:
    print("\n❌ ОШИБКА: Токен не найден в .env файле!")
    sys.exit(1)

# ===== ПРАВИЛЬНЫЙ ФОРМАТ ИЗ ДОКУМЕНТАЦИИ =====
headers = {
    'Content-Type': 'application/vnd.api+json',
    'X-Auth-Token': KASPI_TOKEN
}

# ОБЯЗАТЕЛЬНЫЕ параметры!
params = {
    'page[number]': 0,
    'page[size]': 20
}

url = "https://kaspi.kz/shop/api/v2/orders"

print(f"\n📡 Отправляю запрос...")
print(f"   URL: {url}")
print(f"   Headers: Content-Type, X-Auth-Token")
print(f"   Params: page[number]=0, page[size]=20")
print(f"\n⏳ Ожидание ответа (таймаут 30 сек)...\n")

try:
    response = requests.get(url, headers=headers, params=params, timeout=30)
    
    status = response.status_code
    
    print("=" * 80)
    print(f"📊 РЕЗУЛЬТАТ: HTTP {status}")
    print("=" * 80)
    
    if status == 200:
        print("\n🎉🎉🎉 УСПЕХ! API РАБОТАЕТ! 🎉🎉🎉")
        print("\n✅ Токен правильный")
        print("✅ API активирован")
        print("✅ Запрос корректный")
        
        try:
            data = response.json()
            total_count = data.get('meta', {}).get('totalCount', 0)
            page_count = data.get('meta', {}).get('pageCount', 0)
            orders = data.get('data', [])
            
            print(f"\n📦 СТАТИСТИКА:")
            print(f"   Всего заказов: {total_count}")
            print(f"   Страниц: {page_count}")
            print(f"   На этой странице: {len(orders)}")
            
            if orders:
                print(f"\n📋 ПЕРВЫЙ ЗАКАЗ:")
                first_order = orders[0]
                attrs = first_order.get('attributes', {})
                print(f"   ID: {first_order.get('id')}")
                print(f"   Код: {attrs.get('code')}")
                print(f"   Сумма: {attrs.get('totalPrice')} ₸")
                print(f"   Статус: {attrs.get('status')}")
                print(f"   Состояние: {attrs.get('state')}")
            
        except Exception as e:
            print(f"\n📄 Ответ (текст): {response.text[:500]}")
        
        print("\n" + "=" * 80)
        print("✅ ИНТЕГРАЦИЯ ГОТОВА К РАБОТЕ!")
        print("=" * 80)
        print("\n📝 Следующие шаги:")
        print("   1. Запустите: python Script.py")
        print("   2. Или используйте автозагрузку: python kaspi_auto_uploader.py")
        
    elif status == 400:
        print("\n⚠️ HTTP 400 - BAD REQUEST")
        print("\n❌ Проблема в формате запроса")
        try:
            error = response.json()
            print(f"\n📄 Ошибка от сервера:")
            print(f"   {error}")
        except:
            print(f"\n📄 Текст ответа:")
            print(f"   {response.text[:500]}")
        
        print("\n💡 Возможные причины:")
        print("   • Не хватает обязательных параметров")
        print("   • Неверный формат JSON")
        print("   • Проверьте документацию")
        
    elif status == 401:
        print("\n🔐 HTTP 401 - UNAUTHORIZED")
        print("\n❌ Токен неверный или истёк")
        print(f"\n📄 Ответ: {response.text[:500]}")
        print("\n💡 Решение:")
        print("   1. Зайдите: https://kaspi.kz/merchantcabinet/")
        print("   2. Настройки → Токен API")
        print("   3. Сформируйте новый токен")
        print("   4. Обновите файл .env")
        
    elif status == 403:
        print("\n🚫 HTTP 403 - FORBIDDEN")
        print("\n❌ Нет прав доступа к API")
        print(f"\n📄 Ответ: {response.text[:500]}")
        print("\n💡 Решение:")
        print("   1. Проверьте активацию API в кабинете")
        print("   2. Убедитесь, что токен для Shop API")
        print("   3. Позвоните: 2323")
        
    else:
        print(f"\n⚠️ НЕОЖИДАННЫЙ КОД: {status}")
        print(f"\n📄 Ответ: {response.text[:500]}")

except requests.Timeout:
    print("=" * 80)
    print("⏰ TIMEOUT - СЕРВЕР НЕ ОТВЕТИЛ")
    print("=" * 80)
    print("\n❌ API не отвечает в течение 30 секунд")
    print("\n💡 Возможные причины:")
    print("   1. API не активирован в кабинете продавца")
    print("   2. Токен для другого сервиса (не Shop API)")
    print("   3. IP-адрес заблокирован")
    print("\n📞 Решение: Позвоните 2323")

except requests.ConnectionError:
    print("\n❌ ОШИБКА СОЕДИНЕНИЯ")
    print("\n💡 Проверьте интернет-подключение")

except Exception as e:
    print(f"\n❌ НЕПРЕДВИДЕННАЯ ОШИБКА")
    print(f"   Тип: {type(e).__name__}")
    print(f"   Сообщение: {str(e)[:500]}")

print("\n" + "=" * 80)
print("📚 Документация: KASPI_API_ПОЛНАЯ_ДОКУМЕНТАЦИЯ_V2.md")
print("=" * 80)
