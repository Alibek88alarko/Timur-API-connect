# 🚀 KASPI API - ШПАРГАЛКА (QUICK START)

**Дата:** 8 октября 2025

---

## ⚡ САМОЕ ВАЖНОЕ

### 1. Токен
```
Кабинет → Настройки → Токен API → Сформировать
```

### 2. Заголовки (для ВСЕХ запросов!)
```http
Content-Type: application/vnd.api+json
X-Auth-Token: ваш_токен
```

### 3. Обязательные параметры для списков
```
page[number]=0
page[size]=20
```
**БЕЗ ЭТИХ ПАРАМЕТРОВ = HTTP 400!**

---

## 📋 ПОЛУЧИТЬ ЗАКАЗЫ

```python
import requests

headers = {
    'Content-Type': 'application/vnd.api+json',
    'X-Auth-Token': 'ваш_токен'
}

params = {
    'page[number]': 0,  # ОБЯЗАТЕЛЬНО!
    'page[size]': 20    # ОБЯЗАТЕЛЬНО!
}

response = requests.get(
    'https://kaspi.kz/shop/api/v2/orders',
    headers=headers,
    params=params,
    timeout=30
)

print(response.status_code)  # 200 = OK
data = response.json()
print(f"Заказов: {data['meta']['totalCount']}")
```

---

## 🔍 ФИЛЬТРЫ

### Только новые заказы:
```python
params = {
    'page[number]': 0,
    'page[size]': 20,
    'filter[orders][state]': 'NEW',
    'filter[orders][status]': 'APPROVED_BY_BANK'
}
```

### По дате:
```python
import time

timestamp_now = int(time.time() * 1000)
timestamp_yesterday = timestamp_now - (24 * 60 * 60 * 1000)

params = {
    'page[number]': 0,
    'page[size]': 20,
    'filter[orders][creationDate][$ge]': timestamp_yesterday,
    'filter[orders][creationDate][$le]': timestamp_now
}
```

---

## ✅ ПРИНЯТЬ ЗАКАЗ

```python
import requests

headers = {
    'Content-Type': 'application/vnd.api+json',
    'X-Auth-Token': 'ваш_токен'
}

body = {
    "data": {
        "type": "orders",
        "id": "order_id_здесь",
        "attributes": {
            "code": "номер_заказа",
            "status": "ACCEPTED_BY_MERCHANT"
        }
    }
}

response = requests.post(
    'https://kaspi.kz/shop/api/v2/orders',
    headers=headers,
    json=body
)
```

---

## ❌ ОТМЕНИТЬ ЗАКАЗ

```python
body = {
    "data": {
        "type": "orders",
        "id": "order_id",
        "attributes": {
            "code": "номер_заказа",
            "status": "CANCELLED",
            "cancellationReason": "MERCHANT_OUT_OF_STOCK",
            "cancellationComment": "Нет в наличии"
        }
    }
}
```

**Причины отмены:**
- `MERCHANT_OUT_OF_STOCK` - нет в наличии
- `BUYER_CANCELLATION_BY_MERCHANT` - отказ покупателя
- `BUYER_NOT_REACHABLE` - не дозвонились

---

## 📦 ПОЛУЧИТЬ СОСТАВ ЗАКАЗА

```python
order_id = "abc123"  # ID из списка заказов

response = requests.get(
    f'https://kaspi.kz/shop/api/v2/orders/{order_id}/entries',
    headers=headers
)

items = response.json()['data']
for item in items:
    print(f"Товар: {item['attributes']['category']['title']}")
    print(f"Цена: {item['attributes']['totalPrice']} ₸")
```

---

## 🏪 ДОБАВИТЬ ТОВАР

```python
headers = {
    'Accept': 'application/json',
    'X-Auth-Token': 'ваш_токен',
    'Content-Type': 'text/plain'
}

body = [
    {
        "sku": "SKU123",
        "title": "Название товара",
        "brand": "Бренд",
        "category": "Master - Blenders",
        "description": "Описание",
        "attributes": [
            {
                "code": "код_характеристики",
                "value": "значение"
            }
        ],
        "images": [
            {"url": "https://example.com/image.jpg"}
        ]
    }
]

response = requests.post(
    'https://kaspi.kz/shop/api/products/import',
    headers=headers,
    json=body
)
```

---

## 🗂️ ПОЛУЧИТЬ КАТЕГОРИИ

```python
headers = {
    'Accept': 'application/json',
    'X-Auth-Token': 'ваш_токен'
}

response = requests.get(
    'https://kaspi.kz/shop/api/products/classification/categories',
    headers=headers
)

categories = response.json()
for cat in categories:
    print(f"{cat['code']} - {cat['title']}")
```

---

## ⚠️ КОДЫ ОТВЕТОВ

| Код | Что делать |
|-----|-----------|
| 200 | ✅ Всё ОК, продолжайте |
| 400 | ⚠️ Проверьте параметры (особенно page[number] и page[size]) |
| 401 | 🔐 Получите новый токен в кабинете |
| 403 | 🚫 Проверьте активацию API, звоните 2323 |
| Timeout | ❌ API не активирован, звоните 2323 |

---

## 🐛 TROUBLESHOOTING

### Получаю HTTP 400
```
✓ Добавьте page[number]=0 и page[size]=20
✓ Проверьте JSON на валидность
✓ Убедитесь в Content-Type
```

### Получаю Timeout
```
✓ Проверьте токен в кабинете
✓ Убедитесь, что API активирован
✓ Позвоните 2323
```

### Получаю HTTP 401
```
✓ Получите новый токен
✓ Проверьте формат токена (Base64)
✓ Убедитесь, что токен для Shop API
```

---

## 📞 ПОДДЕРЖКА

**Телефон:** 2323 (бесплатно, 24/7)  
**Кабинет:** https://kaspi.kz/merchantcabinet/  
**Документация:** KASPI_API_ПОЛНАЯ_ДОКУМЕНТАЦИЯ_V2.md

---

## 💾 .ENV ФАЙЛ

```env
AL_STYLE_TOKEN=ваш_токен_al_style
KASPI_TOKEN=ваш_токен_kaspi
```

---

**Версия:** 2.0 | **Дата:** 08.10.2025 | **Статус:** ✅ Актуально
