#!/usr/bin/env python3
"""
ПРОДВИНУТАЯ ПРОВЕРКА ТОКЕНА KASPI
Пробуем ВСЕ возможные варианты из документации
"""
import requests
import os
import base64
from dotenv import load_dotenv

load_dotenv()

KASPI_TOKEN = os.getenv('KASPI_TOKEN')

print("=" * 80)
print("🔬 ПРОДВИНУТАЯ ДИАГНОСТИКА ТОКЕНА KASPI")
print("=" * 80)
print(f"\n🔑 Токен: {KASPI_TOKEN[:30]}..." if KASPI_TOKEN else "❌ Токен не найден")

# ВАРИАНТЫ 1: Разные версии API
print("\n" + "=" * 80)
print("📍 ТЕСТ 1: РАЗНЫЕ ВЕРСИИ API")
print("=" * 80)

api_versions = [
    ("v2 (текущая)", "https://kaspi.kz/shop/api/v2/orders", {"X-Auth-Token": KASPI_TOKEN}),
    ("v1 (старая)", "https://kaspi.kz/shop/api/v1/orders", {"X-Auth-Token": KASPI_TOKEN}),
    ("без версии", "https://kaspi.kz/shop/api/orders", {"X-Auth-Token": KASPI_TOKEN}),
]

for name, url, headers in api_versions:
    print(f"\n🔹 {name}: {url}")
    try:
        r = requests.get(url, headers=headers, timeout=3)
        print(f"   ✅ HTTP {r.status_code}")
        if r.status_code != 404:
            print(f"   📄 {r.text[:150]}")
    except requests.Timeout:
        print(f"   ⏰ TIMEOUT")
    except Exception as e:
        print(f"   ❌ {type(e).__name__}")

# ВАРИАНТ 2: Разные форматы заголовков (ИЗ ОФИЦИАЛЬНОЙ ДОКУМЕНТАЦИИ)
print("\n" + "=" * 80)
print("📍 ТЕСТ 2: ФОРМАТЫ ЗАГОЛОВКОВ ИЗ ДОКУМЕНТАЦИИ")
print("=" * 80)

header_variants = [
    ("Стандарт vnd.api+json", {
        "Content-Type": "application/vnd.api+json",
        "X-Auth-Token": KASPI_TOKEN
    }),
    ("Только X-Auth-Token", {
        "X-Auth-Token": KASPI_TOKEN
    }),
    ("С Accept заголовком", {
        "Accept": "application/vnd.api+json",
        "X-Auth-Token": KASPI_TOKEN
    }),
    ("Полный набор", {
        "Content-Type": "application/vnd.api+json",
        "Accept": "application/vnd.api+json",
        "X-Auth-Token": KASPI_TOKEN
    }),
]

url = "https://kaspi.kz/shop/api/v2/orders"
for name, headers in header_variants:
    print(f"\n🔹 {name}")
    print(f"   Заголовки: {list(headers.keys())}")
    try:
        r = requests.get(url, headers=headers, params={"page[size]": 1}, timeout=3)
        print(f"   ✅ HTTP {r.status_code}")
        if r.status_code == 200:
            print(f"   🎉 РАБОТАЕТ! Ответ: {r.text[:100]}")
        elif r.status_code in [401, 403]:
            print(f"   🔐 Ошибка авторизации: {r.text[:200]}")
    except requests.Timeout:
        print(f"   ⏰ TIMEOUT")
    except Exception as e:
        print(f"   ❌ {type(e).__name__}")

# ВАРИАНТ 3: Попробуем OPTIONS (узнать, какие методы доступны)
print("\n" + "=" * 80)
print("📍 ТЕСТ 3: OPTIONS ЗАПРОС (узнать доступные методы)")
print("=" * 80)

try:
    print(f"\n🔹 OPTIONS {url}")
    r = requests.options(url, headers={"X-Auth-Token": KASPI_TOKEN}, timeout=3)
    print(f"   ✅ HTTP {r.status_code}")
    print(f"   📋 Allow: {r.headers.get('Allow', 'не указано')}")
    print(f"   📋 Headers: {dict(r.headers)}")
except requests.Timeout:
    print(f"   ⏰ TIMEOUT")
except Exception as e:
    print(f"   ❌ {type(e).__name__}")

# ВАРИАНТ 4: HEAD запрос (легковесная проверка)
print("\n" + "=" * 80)
print("📍 ТЕСТ 4: HEAD ЗАПРОС (легковесная проверка)")
print("=" * 80)

try:
    print(f"\n🔹 HEAD {url}")
    r = requests.head(url, headers={"X-Auth-Token": KASPI_TOKEN}, timeout=3)
    print(f"   ✅ HTTP {r.status_code}")
    print(f"   📋 Headers: {dict(r.headers)}")
except requests.Timeout:
    print(f"   ⏰ TIMEOUT")
except Exception as e:
    print(f"   ❌ {type(e).__name__}")

# ВАРИАНТ 5: Проверка токена через base64
print("\n" + "=" * 80)
print("📍 ТЕСТ 5: АНАЛИЗ ФОРМАТА ТОКЕНА")
print("=" * 80)

print(f"\n🔹 Оригинальный токен:")
print(f"   Длина: {len(KASPI_TOKEN)} символов")
print(f"   Формат: Base64 (заканчивается на '=')")
print(f"   Значение: {KASPI_TOKEN}")

# Попробуем декодировать (может токен нужно использовать декодированным?)
try:
    decoded = base64.b64decode(KASPI_TOKEN)
    print(f"\n🔹 Декодированный токен:")
    print(f"   Байт: {len(decoded)} байт")
    print(f"   Hex: {decoded.hex()}")
    print(f"   Пробуем с декодированным...")
    
    # Тест с декодированным токеном
    r = requests.get(
        "https://kaspi.kz/shop/api/v2/orders",
        headers={"X-Auth-Token": decoded.hex()},
        params={"page[size]": 1},
        timeout=3
    )
    print(f"   ✅ HTTP {r.status_code}")
except requests.Timeout:
    print(f"   ⏰ TIMEOUT")
except Exception as e:
    print(f"   ℹ️ Декодирование не помогло")

# ВАРИАНТ 6: Попробуем без HTTPS (может быть редирект?)
print("\n" + "=" * 80)
print("📍 ТЕСТ 6: HTTP vs HTTPS")
print("=" * 80)

for protocol in ["https", "http"]:
    print(f"\n🔹 {protocol.upper()}")
    try:
        test_url = f"{protocol}://kaspi.kz/shop/api/v2/orders"
        r = requests.get(
            test_url,
            headers={"X-Auth-Token": KASPI_TOKEN},
            params={"page[size]": 1},
            timeout=3,
            allow_redirects=False
        )
        print(f"   ✅ HTTP {r.status_code}")
        if r.status_code in [301, 302, 307, 308]:
            print(f"   🔄 Редирект на: {r.headers.get('Location')}")
    except requests.Timeout:
        print(f"   ⏰ TIMEOUT")
    except Exception as e:
        print(f"   ❌ {type(e).__name__}")

# ФИНАЛЬНЫЕ ВЫВОДЫ
print("\n" + "=" * 80)
print("📊 ИТОГОВЫЕ ВЫВОДЫ")
print("=" * 80)

print("""
ℹ️ Если ВСЕ тесты дали TIMEOUT:
   → API физически не отвечает
   → Возможно, нужна активация через тех. поддержку
   → Или ваш IP-адрес заблокирован

ℹ️ Если получили 401/403:
   → API работает, но токен неверный/нет прав
   → Попросите новый токен в кабинете

ℹ️ Если получили 200:
   → 🎉 ВСЁ РАБОТАЕТ! Используйте этот вариант!

ℹ️ Если получили 404:
   → Endpoint не существует
   → Проверьте документацию
""")

print("\n💡 СЛЕДУЮЩИЙ ШАГ:")
print("   Если ничего не помогло - попробуйте:")
print("   1. Создать НОВЫЙ токен в кабинете")
print("   2. Написать в чат поддержки: https://kaspi.kz/merchantcabinet/support")
print("   3. Проверить, есть ли у вас Premium аккаунт (API может требовать)")
print("=" * 80)
