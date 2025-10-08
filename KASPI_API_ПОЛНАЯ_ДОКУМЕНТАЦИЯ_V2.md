# 📚 KASPI.KZ SHOP API - ПОЛНАЯ ДОКУМЕНТАЦИЯ V2.0

**Дата создания:** 8 октября 2025  
**Источник:** Официальная документация guide.kaspi.kz  
**Версия API:** v2

---

## 🔑 АВТОРИЗАЦИЯ

### Генерация токена:
1. Зайдите в кабинет продавца: https://kaspi.kz/merchantcabinet/
2. Перейдите: **Настройки → Токен API**
3. Нажмите **«Сформировать»**
4. Скопируйте токен (формат: Base64, ~44 символа, заканчивается на `=`)

### Использование токена:
```
X-Auth-Token: ваш_токен_здесь
```

---

## 📋 ОБЯЗАТЕЛЬНЫЕ ЗАГОЛОВКИ

Для **ВСЕХ** запросов:
```http
Content-Type: application/vnd.api+json
X-Auth-Token: ваш_токен
```

Для некоторых запросов дополнительно:
```http
Accept: application/vnd.api+json
```

---

## 🛒 ORDERS API (Заказы)

### 1. Получить список заказов

**Endpoint:**
```http
GET https://kaspi.kz/shop/api/v2/orders
```

**⚠️ ОБЯЗАТЕЛЬНЫЕ параметры:**
- `page[number]` - номер страницы (начинается с 0)
- `page[size]` - количество заказов на странице (макс. 100)

**Опциональные параметры:**

| Параметр | Значения | Описание |
|----------|----------|----------|
| `filter[orders][state]` | NEW, SIGN_REQUIRED, PICKUP, DELIVERY, KASPI_DELIVERY, ARCHIVE | Состояние заказа |
| `filter[orders][status]` | APPROVED_BY_BANK, ACCEPTED_BY_MERCHANT, COMPLETED, CANCELLED, CANCELLING, KASPI_DELIVERY_RETURN_REQUESTED, RETURNED | Статус заказа |
| `filter[orders][creationDate][$ge]` | миллисекунды | Дата создания (от) |
| `filter[orders][creationDate][$le]` | миллисекунды | Дата создания (до) |
| `filter[orders][deliveryType]` | DELIVERY, KASPI_DELIVERY, PICKUP | Способ доставки |
| `filter[orders][signatureRequired]` | true, false | Подписание документов |
| `include[orders]` | user | Информация о покупателе |

**Пример запроса:**
```http
GET https://kaspi.kz/shop/api/v2/orders?page[number]=0&page[size]=20&filter[orders][state]=NEW&filter[orders][status]=APPROVED_BY_BANK
Content-Type: application/vnd.api+json
X-Auth-Token: ваш_токен
```

**Пример ответа (200 OK):**
```json
{
  "data": [
    {
      "type": "orders",
      "id": "orderID",
      "attributes": {
        "code": "1234567890",
        "totalPrice": 96045,
        "customer": {
          "firstName": "Иван",
          "lastName": "Иванов",
          "cellPhone": "7xx0xxxxxx"
        },
        "deliveryMode": "DELIVERY_PICKUP",
        "paymentMode": "PAY_WITH_CREDIT",
        "state": "PICKUP",
        "status": "ACCEPTED_BY_MERCHANT",
        "creationDate": 1479470446241
      }
    }
  ],
  "meta": {
    "pageCount": 1,
    "totalCount": 1
  }
}
```

---

### 2. Получить заказ по коду

**Endpoint:**
```http
GET https://kaspi.kz/shop/api/v2/orders?filter[orders][code]=ordercode
```

**Параметры:**
- `filter[orders][code]` - номер заказа

**Пример:**
```http
GET https://kaspi.kz/shop/api/v2/orders?filter[orders][code]=1234567890
Content-Type: application/vnd.api+json
X-Auth-Token: ваш_токен
```

---

### 3. Получить товары в заказе

**Endpoint:**
```http
GET https://kaspi.kz/shop/api/v2/orders/{orderID}/entries
```

**Параметры:**
- `{orderID}` - уникальный ID заказа (из атрибута `id`)

**Пример:**
```http
GET https://kaspi.kz/shop/api/v2/orders/abc123def456/entries
Content-Type: application/vnd.api+json
X-Auth-Token: ваш_токен
```

**Ответ:**
```json
{
  "data": [
    {
      "type": "orderentries",
      "id": "entryID",
      "attributes": {
        "quantity": 2,
        "totalPrice": 4000.0,
        "basePrice": 2000.0,
        "category": {
          "code": "Master - Fruits",
          "title": "Фрукты"
        }
      }
    }
  ]
}
```

---

### 4. Принять заказ

**Endpoint:**
```http
POST https://kaspi.kz/shop/api/v2/orders
```

**Body:**
```json
{
  "data": {
    "type": "orders",
    "id": "orderID",
    "attributes": {
      "code": "ordercode",
      "status": "ACCEPTED_BY_MERCHANT"
    }
  }
}
```

---

### 5. Изменить статус заказа

**Endpoint:**
```http
POST https://kaspi.kz/shop/api/v2/orders
```

**Доступные статусы:**

| Статус | Описание | Когда использовать |
|--------|----------|-------------------|
| `ACCEPTED_BY_MERCHANT` | Принят продавцом | После получения заказа |
| `COMPLETED` | Выдан покупателю | После выдачи (требует код подтверждения) |
| `CANCELLED` | Отменен | При отмене заказа |
| `ARRIVED` | Прибыл на склад | Для предзаказов |
| `ASSEMBLE` | Скомплектован | Для Kaspi Доставки |

**Пример - отмена заказа:**
```json
{
  "data": {
    "type": "orders",
    "id": "orderID",
    "attributes": {
      "code": "ordercode",
      "status": "CANCELLED",
      "cancellationReason": "MERCHANT_OUT_OF_STOCK",
      "cancellationComment": "Товара нет в наличии"
    }
  }
}
```

**Причины отмены:**
- `BUYER_CANCELLATION_BY_MERCHANT` - отказ покупателя
- `BUYER_NOT_REACHABLE` - не удалось связаться
- `MERCHANT_OUT_OF_STOCK` - нет в наличии

---

### 6. Завершить заказ (выдать покупателю)

**Шаг 1 - отправить код покупателю:**
```http
POST https://kaspi.kz/shop/api/v2/orders
X-Auth-Token: token
X-Security-Code: 
X-Send-Code: true
Content-Type: application/vnd.api+json

{
  "data": {
    "type": "orders",
    "id": "orderID",
    "attributes": {
      "code": "ordercode",
      "status": "COMPLETED"
    }
  }
}
```

**Шаг 2 - завершить с кодом от покупателя:**
```http
POST https://kaspi.kz/shop/api/v2/orders
X-Auth-Token: token
X-Security-Code: 1234
X-Send-Code: true
Content-Type: application/vnd.api+json

{
  "data": {
    "type": "orders",
    "id": "orderID",
    "attributes": {
      "code": "ordercode",
      "status": "COMPLETED"
    }
  }
}
```

---

### 7. Указать IMEI-код устройства

**Endpoint:**
```http
POST https://kaspi.kz/shop/api/v2/orderEntryImeiOperation
```

**Body (одно устройство с двумя SIM):**
```json
{
  "data": {
    "type": "orderEntryImeiOperation",
    "attributes": {
      "items": [
        {
          "imei": ["imei1", "imei2"]
        }
      ]
    },
    "relationships": {
      "entry": {
        "data": {
          "type": "orderentries",
          "id": "entryID"
        }
      }
    }
  }
}
```

---

### 8. Получить IMEI-коды в заказе

**Endpoint:**
```http
GET https://kaspi.kz/shop/api/v2/orders/{orderID}/imei
```

---

## 📦 PRODUCTS API (Товары)

### 1. Добавить товар

**Endpoint:**
```http
POST https://kaspi.kz/shop/api/products/import
```

**Headers:**
```http
Accept: application/json
X-Auth-Token: token
Content-Type: text/plain
```

**Body:**
```json
[
  {
    "sku": "SKU123",
    "title": "Название товара",
    "brand": "Бренд",
    "category": "Master - Exercise notebooks",
    "description": "Описание",
    "attributes": [
      {
        "code": "Exercise notebooks*Obsie harakteristiki.exercise notebooks*type",
        "value": "тетрадь-блокнот"
      }
    ],
    "images": [
      {
        "url": "https://example.com/image.jpg"
      }
    ]
  }
]
```

---

### 2. Получить список категорий

**Endpoint:**
```http
GET https://kaspi.kz/shop/api/products/classification/categories
```

**Headers:**
```http
Accept: application/json
X-Auth-Token: token
```

**Ответ:**
```json
[
  {
    "code": "Master - Exercise notebooks",
    "title": "Тетради"
  },
  {
    "code": "Master - Blenders",
    "title": "Блендеры"
  }
]
```

---

### 3. Получить характеристики категории

**Endpoint:**
```http
GET https://kaspi.kz/shop/api/products/classification/attributes?c=Master - Exercise notebooks
```

**Параметры:**
- `c` - код категории

**Ответ:**
```json
[
  {
    "code": "Exercise notebooks*Obsie harakteristiki.exercise notebooks*type",
    "type": "enum",
    "multiValued": false,
    "mandatory": true
  }
]
```

---

### 4. Получить значения характеристики

**Endpoint:**
```http
GET https://kaspi.kz/shop/api/products/classification/attribute/values?c=Master - Exercise notebooks&a=Exercise notebooks*Obsie harakteristiki.exercise notebooks*cover
```

**Параметры:**
- `c` - код категории
- `a` - код характеристики

**Ответ:**
```json
[
  {
    "code": "мягкая",
    "name": "мягкая"
  },
  {
    "code": "твердая",
    "name": "твердая"
  }
]
```

---

### 5. Проверить результат загрузки товара

**Endpoint:**
```http
GET https://kaspi.kz/shop/api/products/import/result?i=upload_code
```

**Параметры:**
- `i` - код загрузки (из ответа при добавлении товара)

**Ответ:**
```json
{
  "errors": 0,
  "warnings": 0,
  "skipped": 0,
  "total": 1,
  "result": {
    "SKU123": {
      "state": "FINISHED"
    }
  }
}
```

---

## 📍 WAREHOUSES API (Склады)

### Получить информацию о складе

**Endpoint:**
```http
GET https://kaspi.kz/shop/api/v2/pointofservices/{pointOfServiceId}
```

**Ответ:**
```json
{
  "data": {
    "type": "pointofservices",
    "id": "warehouseID",
    "attributes": {
      "address": {
        "streetName": "улица Сатпаева",
        "streetNumber": "22/1",
        "town": "г. Алматы",
        "formattedAddress": "г. Алматы, улица Сатпаева, 22/1",
        "latitude": 43.236625,
        "longitude": 76.933373
      },
      "displayName": "PP1"
    }
  }
}
```

---

## ⚠️ КОДЫ ОТВЕТОВ

| Код | Название | Описание | Действие |
|-----|----------|----------|----------|
| 200 | OK | Успешно | Продолжайте работу |
| 400 | Bad Request | Неверный формат запроса | Проверьте параметры, обязательные поля |
| 401 | Unauthorized | Неверный токен | Получите новый токен |
| 403 | Forbidden | Нет прав | Проверьте активацию API |
| 404 | Not Found | Endpoint не найден | Проверьте URL |
| 500 | Server Error | Ошибка сервера | Повторите позже |

---

## 🔥 ЧАСТЫЕ ОШИБКИ И РЕШЕНИЯ

### Ошибка: HTTP 400 Bad Request

**Причины:**
1. Не указаны обязательные параметры `page[number]` и `page[size]`
2. Неверный формат JSON в теле запроса
3. Отсутствуют обязательные атрибуты
4. Неверное значение параметра

**Решение:**
- Всегда указывайте `page[number]=0&page[size]=20` для списков
- Проверьте JSON на валидность
- Сверьтесь с примерами из документации

---

### Ошибка: HTTP 401 Unauthorized

**Причины:**
1. Токен неверный
2. Токен истёк
3. Токен не для Shop API

**Решение:**
1. Зайдите в кабинет: https://kaspi.kz/merchantcabinet/
2. Настройки → Токен API → Сформировать
3. Скопируйте НОВЫЙ токен
4. Обновите файл `.env`

---

### Ошибка: Timeout

**Причины:**
1. API не активирован
2. Токен для другого сервиса (не Shop API)
3. IP-адрес заблокирован

**Решение:**
1. Проверьте активацию API в кабинете
2. Убедитесь, что токен для "Магазина на Kaspi.kz"
3. Позвоните: 2323

---

## 📞 ПОДДЕРЖКА

- **Телефон:** 2323 (круглосуточно, бесплатно)
- **Email:** support@kaspi.kz
- **Кабинет:** https://kaspi.kz/merchantcabinet/
- **Документация:** https://guide.kaspi.kz/partner/ru/shop/api/

---

## 💡 ПОЛЕЗНЫЕ СОВЕТЫ

1. **Всегда используйте пагинацию** - `page[number]` и `page[size]` обязательны
2. **Максимум 100 заказов** на странице
3. **IMEI-коды** обязательны для телефонов
4. **Код подтверждения** нужен для выдачи заказа
5. **Дата в миллисекундах** - используйте timestamp
6. **Content-Type** должен быть `application/vnd.api+json`
7. **Храните токен в безопасности** - не публикуйте в коде

---

## 🎯 БЫСТРЫЙ СТАРТ

### Шаг 1: Получите токен
```
Кабинет → Настройки → Токен API → Сформировать
```

### Шаг 2: Тестовый запрос
```python
import requests

headers = {
    'Content-Type': 'application/vnd.api+json',
    'X-Auth-Token': 'ваш_токен'
}

params = {
    'page[number]': 0,
    'page[size]': 20
}

response = requests.get(
    'https://kaspi.kz/shop/api/v2/orders',
    headers=headers,
    params=params
)

print(response.status_code)  # Должно быть 200
print(response.json())
```

### Шаг 3: Проверьте ответ
- `200` = ✅ Всё работает!
- `400` = ⚠️ Проверьте параметры
- `401` = 🔐 Проверьте токен
- `Timeout` = ❌ API не активирован

---

**Дата обновления:** 8 октября 2025  
**Версия:** 2.0  
**Статус:** Актуально ✅
