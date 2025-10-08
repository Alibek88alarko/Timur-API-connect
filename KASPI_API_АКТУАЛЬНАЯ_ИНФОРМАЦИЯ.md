# 📋 АКТУАЛЬНАЯ ИНФОРМАЦИЯ ПО KASPI API (2025)

## 🔍 ИСТОЧНИКИ ИНФОРМАЦИИ:

### ✅ **Официальные ресурсы Kaspi:**
1. **Kaspi Гид для Партнеров**: https://guide.kaspi.kz/partner/ru/shop/api/
2. **Раздел API - Общие вопросы**: https://guide.kaspi.kz/partner/ru/shop/api/general
3. **Раздел API - Заказы**: https://guide.kaspi.kz/partner/ru/shop/api/orders
4. **Раздел API - Товары**: https://guide.kaspi.kz/partner/ru/shop/api/goods
5. **Кабинет продавца**: https://kaspi.kz/merchantcabinet/ (требует авторизации)
6. **Локальный файл**: kaspi API instructions.txt (2157 строк детальной документации)

---

## 🔑 ГЛАВНОЕ: ПРАВИЛЬНЫЕ ENDPOINT'Ы

### **БАЗОВЫЙ URL ДЛЯ API:**
```
Host: kaspi.kz
Base URL: /shop/api/v2
```

### **ВАЖНО! Полный путь:**
```
https://kaspi.kz/shop/api/v2/orders
https://kaspi.kz/shop/api/v2/products
```

**НЕ** `https://kaspi.kz/shop/api/v2` (без /orders или /products)

---

## 🔐 АУТЕНТИФИКАЦИЯ:

### **Заголовки для всех запросов:**
```http
Content-Type: application/vnd.api+json
X-Auth-Token: <Ваш_токен>
```

### **Как получить токен:**
1. Зайдите в кабинет продавца: https://kaspi.kz/merchantcabinet/
2. Перейдите в раздел: **Настройки → API → Токен авторизации**
3. Скопируйте токен (формат: base64 строка ~44 символа)

**Ваш текущий токен:**
```
56Pj6wkGBX34/05TUMV1ptxrGCa1ZdMkderQA1+Gtr0=
```

---

## 📦 РАБОТА С ЗАКАЗАМИ:

### **1. Получение списка заказов:**

**Endpoint:**
```http
GET /shop/api/v2/orders
Host: kaspi.kz
Content-Type: application/vnd.api+json
X-Auth-Token: <токен>
```

**Параметры:**
| Параметр | Описание | Пример |
|----------|----------|--------|
| `page[number]` | Номер страницы (с 0) | 0 |
| `page[size]` | Кол-во заказов (макс 100) | 20 |
| `filter[orders][state]` | NEW, PICKUP, DELIVERY, etc | NEW |
| `filter[orders][status]` | APPROVED_BY_BANK, ACCEPTED_BY_MERCHANT, etc | APPROVED_BY_BANK |
| `filter[orders][creationDate][$ge]` | Дата от (миллисекунды) | 1478736000000 |
| `filter[orders][creationDate][$le]` | Дата до (миллисекунды) | 1479945600000 |

**Статусы заказов:**
- `APPROVED_BY_BANK` - Новый заказ, нужно принять ✅
- `ACCEPTED_BY_MERCHANT` - Принят продавцом
- `COMPLETED` - Завершен
- `CANCELLED` - Отменен
- `CANCELLING` - В процессе отмены
- `KASPI_DELIVERY_RETURN_REQUESTED` - Ожидает возврата
- `RETURNED` - Возвращен

**Состояния заказов:**
- `NEW` - Новый
- `SIGN_REQUIRED` - Нужно подписать документы
- `PICKUP` - Самовывоз
- `DELIVERY` - Ваша доставка
- `KASPI_DELIVERY` - Kaspi Доставка
- `ARCHIVE` - Архивный

**Пример полного запроса:**
```http
GET /shop/api/v2/orders?page[number]=0&page[size]=20&filter[orders][status]=APPROVED_BY_BANK
Host: kaspi.kz
Content-Type: application/vnd.api+json
X-Auth-Token: 56Pj6wkGBX34/05TUMV1ptxrGCa1ZdMkderQA1+Gtr0=
```

---

### **2. Принятие заказа:**

**Endpoint:**
```http
POST /shop/api/v2/orders
Host: kaspi.kz
Content-Type: application/vnd.api+json
X-Auth-Token: <токен>
```

**Тело запроса:**
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

### **3. Отмена заказа:**

**Endpoint:**
```http
POST /shop/api/v2/orders
Host: kaspi.kz
Content-Type: application/vnd.api+json
X-Auth-Token: <токен>
```

**Тело запроса:**
```json
{
  "data": {
    "type": "orders",
    "id": "orderID",
    "attributes": {
      "code": "ordercode",
      "status": "CANCELLED",
      "cancellationReason": "MERCHANT_OUT_OF_STOCK"
    }
  }
}
```

**Причины отмены:**
- `BUYER_CANCELLATION_BY_MERCHANT` - Отказ покупателя
- `BUYER_NOT_REACHABLE` - Не удалось связаться
- `MERCHANT_OUT_OF_STOCK` - Товара нет в наличии

---

### **4. Завершение заказа (статус "Выдан"):**

**Этап 1: Отправка кода покупателю**
```http
POST /shop/api/v2/orders
Host: kaspi.kz
Content-Type: application/vnd.api+json
X-Auth-Token: <токен>
X-Security-Code:
X-Send-Code: true
```

**Этап 2: Подтверждение с кодом от покупателя**
```http
POST /shop/api/v2/orders
Host: kaspi.kz
Content-Type: application/vnd.api+json
X-Auth-Token: <токен>
X-Security-Code: 1234
X-Send-Code: true
```

**Тело запроса (оба этапа):**
```json
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

### **5. Получение информации о составе заказа:**

**Endpoint:**
```http
GET /shop/api/v2/orders/{orderID}/entries
Host: kaspi.kz
Content-Type: application/vnd.api+json
X-Auth-Token: <токен>
```

---

## 📦 РАБОТА С ТОВАРАМИ (XML ПРАЙС-ЛИСТ):

### **Автоматическая загрузка прайс-листа:**

Kaspi автоматически загружает ваш XML прайс-лист **каждые 60 минут**, если есть изменения.

**Настройка в кабинете:**
1. Кабинет продавца → Товары → Загрузить прайс-лист
2. Выбрать "Автоматическая загрузка"
3. Указать URL вашего XML файла

**Структура XML файла:**

```xml
<?xml version="1.0" encoding="utf-8"?>
<kaspi_catalog date="2025-10-08T12:00:00"
              xmlns="kaspiShopping"
          xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
 xsi:schemaLocation="kaspiShopping http://kaspi.kz/kaspishopping.xsd">
   <company>Al-Style</company>
   <merchantid>01</merchantid>
   <offers>
       <offer sku="XK-100UB">
           <model>iPhone 13 Pro 256GB</model>
           <brand>Apple</brand>
           <availabilities>
               <availability 
                 available="yes" 
                 storeId="myFavoritePickupPoint1" 
                 preOrder="0" 
                 stockCount="25"/>
           </availabilities>
           <price>450000</price>
       </offer>
   </offers>
</kaspi_catalog>
```

**Обязательные элементы:**
- `sku` - Артикул (макс 20 символов, уникальный)
- `model` - Название товара
- `brand` - Бренд
- `available` - yes/no
- `storeId` - Код склада (из кабинета)
- `stockCount` - Остатки
- `price` - Цена (целое число, без НДС)

**preOrder** - Количество дней предзаказа (0-30)

**Схема валидации:**
```
http://kaspi.kz/kaspishopping.xsd
```

---

## 🚨 ПРОБЛЕМЫ И РЕШЕНИЯ:

### **Проблема 1: Timeout при подключении**

**Причины:**
1. ❌ Неверный базовый URL
2. ❌ Отсутствует endpoint (/orders)
3. ❌ Токен недействителен
4. ❌ API не активирован в кабинете

**Решение:**
```python
# ❌ НЕПРАВИЛЬНО:
url = "https://kaspi.kz/shop/api/v2"

# ✅ ПРАВИЛЬНО:
url = "https://kaspi.kz/shop/api/v2/orders"
```

---

### **Проблема 2: 401 Unauthorized**

**Причины:**
1. Неверный токен
2. Токен истёк
3. Токен не активирован

**Решение:**
1. Зайдите в кабинет продавца
2. Проверьте токен в разделе API
3. При необходимости создайте новый

---

### **Проблема 3: 403 Forbidden**

**Причины:**
1. API не активирован для вашего аккаунта
2. Нет прав доступа к endpoint

**Решение:**
- Свяжитесь с техподдержкой Kaspi: **2323** (бесплатно)

---

## ✅ ПРОВЕРЕННАЯ КОНФИГУРАЦИЯ:

### **Для вашего проекта:**

```python
# config.py
KASPI_API_URL = "https://kaspi.kz/shop/api/v2"
KASPI_TOKEN = "56Pj6wkGBX34/05TUMV1ptxrGCa1ZdMkderQA1+Gtr0="

KASPI_HEADERS = {
    'Content-Type': 'application/vnd.api+json',
    'X-Auth-Token': KASPI_TOKEN
}

# Endpoints:
ORDERS_ENDPOINT = f"{KASPI_API_URL}/orders"
PRODUCTS_ENDPOINT = f"{KASPI_API_URL}/products"
```

---

## 🔧 СЛЕДУЮЩИЕ ШАГИ:

1. ✅ **Проверить токен** в кабинете продавца
2. ✅ **Убедиться, что API активирован**
3. ✅ **Протестировать подключение** с правильными endpoint'ами
4. ✅ **Проверить доступность** через простой GET запрос
5. ⚠️ **Если не работает** - связаться с техподдержкой 2323

---

## 📞 ТЕХПОДДЕРЖКА:

- **Телефон**: 2323 (бесплатно с мобильного)
- **Чат**: В кабинете продавца
- **Email**: Через форму в кабинете

---

## 📝 ДОПОЛНИТЕЛЬНАЯ ИНФОРМАЦИЯ:

### **Лимиты API:**
- Автоматическая загрузка XML: каждые 60 минут
- Рекомендуемая задержка между запросами: 1-5 секунд

### **Таймауты:**
- Рекомендуемый timeout: 10-30 секунд
- Для заказов: 30 секунд
- Для товаров: 60 секунд

---

**Дата создания отчета**: 2025-10-08
**Источники**: Официальная документация Kaspi + локальные инструкции
