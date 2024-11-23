# Импортируем необходимые библиотеки
import requests  # Для работы с HTTP-запросами
import json      # Для работы с JSON-данными
import time      # Для работы с временем
import logging   # Для логирования

# Настраиваем логирование
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Токены доступа (используются для аутентификации в API)
AL_STYLE_TOKEN = 'fTjmIXfcC0F1F_lykYdkCPOqNJDXp_xm'  # Токен для Al Style
KASPI_TOKEN = '56Pj6wkGBX34/05TUMV1ptxrGCa1ZdMkderQA1+Gtr0='  # Токен для Kaspi.kz

# Базовые URL-адреса API
AL_STYLE_API_URL = 'https://api.al-style.kz/api'  # API-адрес для Al Style
KASPI_API_URL = 'https://kaspi.kz/shop/api/v2'  # API-адрес для Kaspi.kz

# Заголовки для запросов в Al Style
AL_STYLE_HEADERS = {
    'Content-Type': 'application/json',  # Тип содержимого — JSON
    'Accept': 'application/json'         # Ожидаем JSON в ответе
}

# Заголовки для запросов в Kaspi.kz
KASPI_HEADERS = {
    'Content-Type': 'application/vnd.api+json',  # Тип содержимого — специфичный JSON
    'X-Auth-Token': KASPI_TOKEN                 # Передаем токен аутентификации
}

def get_al_style_products():
    """
    Получает список товаров из вашего интернет-магазина.
    """
    logging.info('Начало получения товаров из Al Style')
    # Формируем URL для получения товаров
    url = f"{AL_STYLE_API_URL}/elements-pagination"
    # Параметры запроса (фильтры, лимиты, дополнительные поля)
    params = {
        'access-token': AL_STYLE_TOKEN,  # Токен доступа
        'limit': 100,                    # Количество товаров на запрос
        'offset': 0,                     # Смещение для пагинации
        'additional_fields': 'brand,price1,price2,quantity,article_pn'  # Дополнительные данные о товаре
    }
    all_products = []  # Список для хранения всех товаров

    while True:  # Цикл для получения всех страниц товаров
        # Выполняем запрос
        response = requests.get(url, headers=AL_STYLE_HEADERS, params=params)
        data = response.json()  # Преобразуем ответ в JSON
        products = data.get('elements', [])  # Получаем список товаров
        all_products.extend(products)  # Добавляем товары в общий список
        logging.info(f'Получено {len(products)} товаров, всего загружено {len(all_products)}')

        # Проверяем, есть ли следующая страница
        pagination = data.get('pagination', {})  # Информация о пагинации
        if pagination.get('currentPage') >= pagination.get('totalPages'):  # Если последняя страница
            logging.info('Все товары получены из Al Style')
            break  # Выходим из цикла
        else:
            params['offset'] += params['limit']  # Увеличиваем смещение для следующей страницы
            time.sleep(5)  # Ждем 5 секунд, чтобы не перегружать сервер

    return all_products  # Возвращаем полный список товаров

def update_kaspi_prices_stock(products):
    """
    Обновляет цены и остатки на Kaspi.kz.
    """
    logging.info('Начало обновления цен и остатков на Kaspi.kz')
    # Импортируем модуль для работы с XML
    from xml.etree.ElementTree import Element, SubElement, ElementTree

    # Создаем корневой элемент XML-файла
    kaspi_catalog = Element('kaspi_catalog', {
        'date': time.strftime('%Y-%m-%dT%H:%M:%S'),  # Текущая дата и время
        'xmlns': 'kaspiShopping',                   # Пространство имен для XML
        'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',  # Дополнительные атрибуты
        'xsi:schemaLocation': 'kaspiShopping http://kaspi.kz/kaspishopping.xsd'  # Схема для Kaspi
    })

    # Добавляем информацию о компании
    company = SubElement(kaspi_catalog, 'company')
    company.text = 'Название вашей компании'  # Указываем название компании

    # Добавляем идентификатор компании
    merchantid = SubElement(kaspi_catalog, 'merchantid')
    merchantid.text = 'ID вашей компании'  # Указываем ID компании

    # Создаем секцию предложений (товаров)
    offers = SubElement(kaspi_catalog, 'offers')

    for product in products:  # Проходим по каждому товару
        # Добавляем информацию о товаре (offer)
        offer = SubElement(offers, 'offer', {
            'sku': str(product.get('article_pn', product.get('article')))  # Уникальный код товара
        })

        # Указываем модель товара
        model = SubElement(offer, 'model')
        model.text = product.get('name')  # Название товара

        # Указываем бренд товара
        brand = SubElement(offer, 'brand')
        brand.text = product.get('brand', 'Unknown')  # Бренд или "Unknown"

        # Указываем информацию о доступности на складе
        availabilities = SubElement(offer, 'availabilities')
        availability = SubElement(availabilities, 'availability', {
            'available': 'yes' if product.get('quantity') != '0' else 'no',  # Есть ли в наличии
            'storeId': 'yourStoreId',  # Код склада
            'preOrder': '0',  # Возможность предзаказа
            'stockCount': str(product.get('quantity'))  # Остаток на складе
        })

        # Указываем цену товара
        price = SubElement(offer, 'price')
        price.text = str(product.get('price2'))  # Цена товара

    # Сохраняем XML-файл
    tree = ElementTree(kaspi_catalog)
    tree.write('kaspi_price_list.xml', encoding='utf-8', xml_declaration=True)  # Сохраняем файл
    logging.info('Цены и остатки успешно обновлены на Kaspi.kz')

def process_kaspi_orders():
    """
    Обрабатывает заказы с Kaspi.kz и обновляет остатки в вашем магазине.
    """
    logging.info('Начало обработки заказов с Kaspi.kz')
    # Параметры для фильтрации заказов
    params = {
        'filter[orders][status]': 'APPROVED_BY_BANK',  # Только подтвержденные заказы
        'page[number]': 0,  # Номер страницы
        'page[size]': 20    # Размер страницы (количество заказов)
    }
    # Выполняем запрос на получение заказов
    response = requests.get(f"{KASPI_API_URL}/orders", headers=KASPI_HEADERS, params=params)
    orders = response.json().get('data', [])  # Получаем список заказов
    logging.info(f'Найдено {len(orders)} заказов для обработки')

    for order in orders:  # Проходим по каждому заказу
        order_id = order['id']  # ID заказа
        order_code = order['attributes']['code']  # Код заказа

        # Формируем запрос для принятия заказа
        accept_order_payload = {
            "data": {
                "type": "orders",
                "id": order_id,
                "attributes": {
                    "code": order_code,
                    "status": "ACCEPTED_BY_MERCHANT"  # Меняем статус на "Принят"
                }
            }
        }
        # Отправляем запрос для принятия заказа
        response = requests.post(f"{KASPI_API_URL}/orders", headers=KASPI_HEADERS, json=accept_order_payload)
        if response.status_code == 200:  # Если запрос успешный
            logging.info(f"Заказ {order_code} принят")
        else:
            logging.error(f"Ошибка при принятии заказа {order_code}: {response.status_code}")
            continue  # Переходим к следующему заказу

        # Получаем состав заказа
        entries_link = order['relationships']['entries']['links']['related']
        response_entries = requests.get(entries_link, headers=KASPI_HEADERS)
        entries = response_entries.json().get('data', [])  # Товары из заказа

        for entry in entries:  # Проходим по каждому товару
            product_id = entry['id']  # ID товара
            quantity = entry['attributes']['quantity']  # Количество товара

            # Получаем данные о товаре
            product_link = entry['relationships']['product']['links']['related']
            response_product = requests.get(product_link, headers=KASPI_HEADERS)
            product_data = response_product.json()['data']
            product_code = product_data['attributes']['code']  # Код товара

            # Обновляем остаток в Al Style
            al_style_quantity_url = f"{AL_STYLE_API_URL}/quantity"
            al_style_params = {
                'access-token': AL_STYLE_TOKEN,
                'article': product_code  # Код товара
            }
            response_quantity = requests.get(al_style_quantity_url, headers=AL_STYLE_HEADERS, params=al_style_params)
            if response_quantity.status_code == 200:
                quantity_data = response_quantity.json()  # Текущий остаток
                current_quantity = int(quantity_data.get(product_code, 0))  # Остаток на складе

                # Вычисляем новый остаток
                new_quantity = current_quantity - int(quantity)  # Вычитаем заказанное количество
                if new_quantity < 0:  # Если остаток отрицательный
                    new_quantity = 0  # Устанавливаем в 0

                # Отправляем запрос на обновление остатка
                update_quantity_payload = {
                    'access-token': AL_STYLE_TOKEN,
                    'article': product_code,
                    'quantity': new_quantity
                }
                update_response = requests.post(f"{AL_STYLE_API_URL}/update-quantity", headers=AL_STYLE_HEADERS, json=update_quantity_payload)
                if update_response.status_code == 200:
                    logging.info(f"Остаток товара {product_code} обновлен до {new_quantity}")
                else:
                    logging.error(f"Ошибка при обновлении остатка товара {product_code}")
            else:
                logging.error(f"Ошибка при получении остатка товара {product_code}")

    logging.info('Обработка заказов с Kaspi.kz завершена')

def main():
    # Получаем список товаров из Al Style
    products = get_al_style_products()
    logging.info(f"Получено {len(products)} товаров из вашего интернет-магазина")

    # Обновляем цены и остатки в Kaspi.kz
    update_kaspi_prices_stock(products)
    logging.info("Цены и остатки обновлены на Kaspi.kz")

    # Обрабатываем заказы с Kaspi.kz
    process_kaspi_orders()
    logging.info("Обработка заказов с Kaspi.kz завершена")

if __name__ == "__main__":
    main()  # Запускаем программу
