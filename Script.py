# Импортируем необходимые библиотеки
import requests  # Для работы с HTTP-запросами
import json      # Для работы с JSON-данными
import time      # Для работы с временем
import logging   # Для логирования
import os        # Для работы с файловой системой
from xml_validator import KaspiXMLValidator  # Для валидации XML
from config import config, AL_STYLE_HEADERS, KASPI_HEADERS  # Конфигурация
import os  # Для работы с файловой системой

# Настраиваем логирование
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Валидируем конфигурацию при запуске
try:
    config.validate()
    logging.info("Конфигурация успешно загружена")
except ValueError as e:
    logging.error(f"Ошибка конфигурации: {e}")
    exit(1)

def get_al_style_products():
    """
    Получает список товаров из вашего интернет-магазина.
    """
    logging.info('Начало получения товаров из Al Style')
    # Формируем URL для получения товаров
    url = f"{config.al_style_api_url}/elements-pagination"
    # Параметры запроса (фильтры, лимиты, дополнительные поля)
    params = {
        'access-token': config.al_style_token,  # Токен доступа
        'limit': 20000,                    # Количество товаров на запрос
        'offset': 0,                     # Смещение для пагинации
        'additional_fields': 'brand,price1,price2,quantity,article_pn'  # Дополнительные данные о товаре
    }
    all_products = []  # Список для хранения всех товаро

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
            time.sleep(config.request_delay)  # Ждем настроенное время, чтобы не перегружать сервер

    return all_products  # Возвращаем полный список товаров


def get_valid_stock_count(quantity):
    """
    Преобразует значение количества товара в корректный формат для XML-файла.
    """
    # Проверяем, является ли значение строкой
    if isinstance(quantity, str):
        # Удаляем пробелы с начала и конца строки
        quantity = quantity.strip()
        # Проверяем, содержит ли строка символ '>'
        if '>' in quantity:
            # Если есть символ '>', возвращаем значение '500' (считаем его большим числом)
            return '500'
        # Проверяем, является ли строка числом (содержит только цифры)
        elif quantity.isdigit():
            # Если строка число, возвращаем её как есть
            return quantity
        else:
            # Если строка не число, возвращаем '0' (некорректное значение)
            return '0'
    # Если значение число (int или float)
    elif isinstance(quantity, (int, float)):
        # Преобразуем его в целое число и возвращаем как строку
        return str(int(quantity))
    else:
        # Если значение ни строка, ни число, возвращаем '0' (некорректное значение)
        return '0'
    
    
def update_kaspi_prices_stock(products):
    """
    Обновляет цены и остатки на Kaspi.kz.
    """
    logging.info('Начало обновления цен и остатков на Kaspi.kz')
    # Импортируем модуль для работы с XML
    from xml.etree.ElementTree import Element, SubElement, tostring
    import xml.dom.minidom
    
    # Создаем корневой элемент XML-файла
    kaspi_catalog = Element('kaspi_catalog', {
        'date': time.strftime('%Y-%m-%dT%H:%M:%S'),  # Текущая дата и время
        'xmlns': 'kaspiShopping',                   # Пространство имен для XML
        'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',  # Дополнительные атрибуты
        'xsi:schemaLocation': 'kaspiShopping http://kaspi.kz/kaspishopping.xsd'  # Схема для Kaspi
    })

    # Добавляем информацию о компании
    company = SubElement(kaspi_catalog, 'company')
    company.text = config.company_name  # Указываем название компании

    # Добавляем идентификатор компании
    merchantid = SubElement(kaspi_catalog, 'merchantid')
    merchantid.text = config.merchant_id  # Указываем ID компании

    # Создаем секцию предложений (товаров) - БЕЗ categories
    offers = SubElement(kaspi_catalog, 'offers')

    for product in products:  # Проходим по каждому товару
        sku = str(product.get('article_pn') or product.get('article') or '').strip()
        if not sku:
            logging.warning('Пропуск товара без SKU')
            continue  # Пропускаем товары без SKU
        
        
        offer = SubElement(offers, 'offer', {
            'sku': sku  # Уникальный код товара
        })

        # Указываем модель товара
        model_value = product.get('name')
        model = SubElement(offer, 'model')
        model.text = model_value.strip() if model_value else 'No Name'

        # Указываем бренд товара
        brand_value = product.get('brand')
        brand = SubElement(offer, 'brand')
        brand.text = brand_value.strip() if brand_value else 'Unknown'
        
        # Указываем информацию о доступности на складе
        availabilities = SubElement(offer, 'availabilities')
        stock_count = get_valid_stock_count(product.get('quantity'))
        availability = SubElement(availabilities, 'availability', {
            'available': 'yes' if int(stock_count) > 0 else 'no',
            'storeId': config.store_id,  # Используем настроенный storeId
            'preOrder': '0',
            'stockCount': stock_count
        })

        # Указываем цену товара
        price = SubElement(offer, 'price')
        price_value = product.get('price2') or product.get('price1') or '0'
        price.text = str(price_value).strip()
        
    # Convert to string
    rough_string = tostring(kaspi_catalog, encoding='utf-8')
    reparsed = xml.dom.minidom.parseString(rough_string)
    pretty_xml_as_string = reparsed.toprettyxml(indent="  ")
    
    xml_filename = config.xml_filename
    with open(xml_filename, 'w', encoding='utf-8') as f:
        f.write(pretty_xml_as_string)
    logging.info('Prices and stock successfully updated and saved to XML for Kaspi.kz')
    
    # Валидируем созданный XML
    logging.info('Начало валидации XML против схемы Kaspi.kz')
    validator = KaspiXMLValidator()
    
    # Проверяем структуру XML
    structure_valid, structure_message = validator.check_required_elements(pretty_xml_as_string)
    if not structure_valid:
        logging.error(f'Ошибка структуры XML: {structure_message}')
        return False
    
    # Валидируем против схемы
    schema_valid, schema_message = validator.validate_xml_string(pretty_xml_as_string)
    if schema_valid:
        logging.info(f'XML успешно прошел валидацию: {schema_message}')
    else:
        logging.warning(f'XML не прошел валидацию схемы: {schema_message}')
        logging.warning('XML сохранен, но может быть отклонен Kaspi.kz')
    
    return True
    
    
    """    
    # Сохраняем XML-файл
    tree = ElementTree(kaspi_catalog)
    tree.write('kaspi_price_list.xml', encoding='utf-8', xml_declaration=True)  # Сохраняем файл
    logging.info('Цены и остатки успешно обновлены и добавлены в XML для Kaspi.kz')
    """
    
def process_kaspi_orders():
    """
    Обрабатывает заказы с Kaspi.kz и обновляет остатки в вашем магазине.
    """
    logging.info('Начало обработки заказов с Kaspi.kz')
    
    # ОБЯЗАТЕЛЬНО: Даты для фильтра (максимум 14 дней!)
    import time
    timestamp_now = int(time.time() * 1000)
    timestamp_past = timestamp_now - (config.kaspi_date_range_days * 24 * 60 * 60 * 1000)
    
    # Параметры для фильтрации заказов (ВСЕ обязательные!)
    params = {
        'page[number]': 0,  # Номер страницы (ОБЯЗАТЕЛЬНО)
        'page[size]': config.kaspi_page_size,  # Размер страницы (ОБЯЗАТЕЛЬНО)
        'filter[orders][creationDate][$ge]': str(timestamp_past),  # Дата от (ОБЯЗАТЕЛЬНО!)
        'filter[orders][creationDate][$le]': str(timestamp_now),   # Дата до (ОБЯЗАТЕЛЬНО!)
        'filter[orders][status]': 'APPROVED_BY_BANK',  # Только подтвержденные заказы
    }
    
    try:
        # Выполняем запрос на получение заказов (правильный endpoint)
        response = requests.get(config.kaspi_orders_url, headers=KASPI_HEADERS, params=params, timeout=config.request_timeout)
        logging.info(f'Статус ответа от Kaspi API: {response.status_code}')
        
        if response.status_code != 200:
            logging.error(f'Ошибка при получении заказов: {response.status_code} - {response.text}')
            return
        
        orders = response.json().get('data', [])  # Получаем список заказов
        logging.info(f'Найдено {len(orders)} заказов для обработки')
        
        if len(orders) == 0:
            logging.info('Нет заказов для обработки в статусе APPROVED_BY_BANK')
            return
            
    except requests.exceptions.RequestException as e:
        logging.error(f'Ошибка при подключении к Kaspi API: {e}')
        return
    except Exception as e:
        logging.error(f'Неожиданная ошибка при получении заказов: {e}')
        return

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
        # Отправляем запрос для принятия заказа (правильный endpoint)
        response = requests.post(config.kaspi_orders_url, headers=KASPI_HEADERS, json=accept_order_payload, timeout=config.request_timeout)
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
            al_style_quantity_url = f"{config.al_style_api_url}/quantity"
            al_style_params = {
                'access-token': config.al_style_token,
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
                    'access-token': config.al_style_token,
                    'article': product_code,
                    'quantity': new_quantity
                }
                update_response = requests.post(f"{config.al_style_api_url}/update-quantity", headers=AL_STYLE_HEADERS, json=update_quantity_payload)
                if update_response.status_code == 200:
                    logging.info(f"Остаток товара {product_code} обновлен до {new_quantity}")
                else:
                    logging.error(f"Ошибка при обновлении остатка товара {product_code}")
            else:
                logging.error(f"Ошибка при получении остатка товара {product_code}")

    logging.info('Обработка заказов с Kaspi.kz завершена')

def test_kaspi_orders():
    """
    Тестовая функция для проверки получения заказов с разными статусами
    """
    logging.info('=== ТЕСТ: Проверка заказов с разными статусами ===')
    
    # ОБЯЗАТЕЛЬНО: Даты для фильтра
    import time
    timestamp_now = int(time.time() * 1000)
    timestamp_past = timestamp_now - (config.kaspi_date_range_days * 24 * 60 * 60 * 1000)
    
    # Список возможных статусов для тестирования
    statuses_to_test = [
        'APPROVED_BY_BANK',
        'ACCEPTED_BY_MERCHANT', 
        'KASPI_DELIVERY_RETURN_REQUESTED',
        'COMPLETED',
        'CANCELLED'
    ]
    
    for status in statuses_to_test:
        params = {
            'page[number]': 0,
            'page[size]': 5,
            'filter[orders][creationDate][$ge]': str(timestamp_past),  # ОБЯЗАТЕЛЬНО!
            'filter[orders][creationDate][$le]': str(timestamp_now),   # ОБЯЗАТЕЛЬНО!
            'filter[orders][status]': status,
        }
        
        try:
            response = requests.get(config.kaspi_orders_url, headers=KASPI_HEADERS, params=params, timeout=config.request_timeout)
            logging.info(f'Статус {status}: HTTP {response.status_code}')
            
            if response.status_code == 200:
                orders = response.json().get('data', [])
                logging.info(f'  Найдено {len(orders)} заказов в статусе {status}')
                
                if len(orders) > 0:
                    # Показываем информацию о первом заказе
                    first_order = orders[0]
                    order_code = first_order.get('attributes', {}).get('code', 'N/A')
                    created_at = first_order.get('attributes', {}).get('createdAt', 'N/A')
                    logging.info(f'  Пример заказа: {order_code}, создан: {created_at}')
            else:
                logging.warning(f'  Ошибка получения заказов в статусе {status}: {response.text}')
                
        except Exception as e:
            logging.error(f'  Ошибка при тестировании статуса {status}: {e}')
    
    logging.info('=== КОНЕЦ ТЕСТА ===')

def upload_xml_to_kaspi(xml_file_path):
    """
    Загружает XML файл с товарами в Kaspi.kz
    """
    logging.info('Начало загрузки XML файла в Kaspi.kz')
    
    try:
        # Проверяем, существует ли файл
        if not os.path.exists(xml_file_path):
            logging.error(f'XML файл не найден: {xml_file_path}')
            return False
        
        # Читаем содержимое XML файла
        with open(xml_file_path, 'rb') as xml_file:
            files = {'file': (xml_file_path, xml_file, 'application/xml')}
            
            # Заголовки для загрузки файла
            headers = {
                'X-Auth-Token': config.kaspi_token
            }
            
            # Отправляем файл
            response = requests.post(
                config.kaspi_xml_upload_url,
                files=files,
                headers=headers,
                timeout=config.request_timeout
            )
            
            logging.info(f'Статус загрузки XML: {response.status_code}')
            
            if response.status_code in [200, 201, 202]:
                logging.info('XML файл успешно загружен в Kaspi.kz')
                logging.info(f'Ответ: {response.text}')
                return True
            else:
                logging.error(f'Ошибка при загрузке XML: {response.status_code} - {response.text}')
                return False
                
    except requests.exceptions.RequestException as e:
        logging.error(f'Ошибка при подключении к Kaspi.kz: {e}')
        return False
    except Exception as e:
        logging.error(f'Неожиданная ошибка при загрузке XML: {e}')
        return False

def main():
    """
    Основная функция с поддержкой режимов тестирования
    """
    import sys
    
    # Проверяем аргументы командной строки
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
        
        if mode == 'test-orders':
            # Тестируем только получение заказов
            test_kaspi_orders()
            return
        elif mode == 'test-products':
            # Тестируем только получение товаров
            products = get_al_style_products()
            logging.info(f"Получено {len(products)} товаров из Al-Style")
            return
        elif mode == 'test-xml':
            # Тестируем только генерацию XML
            products = get_al_style_products()
            xml_valid = update_kaspi_prices_stock(products)
            logging.info(f"XML валидация: {'успешно' if xml_valid else 'ошибка'}")
            return
        elif mode == 'upload-xml':
            # Загружаем XML файл в Kaspi.kz
            xml_uploaded = upload_xml_to_kaspi(config.xml_filename)
            logging.info(f"XML загрузка: {'успешно' if xml_uploaded else 'ошибка'}")
            return
        elif mode == 'help':
            print("Доступные режимы:")
            print("  python Script.py test-orders    - тестировать получение заказов")
            print("  python Script.py test-products  - тестировать получение товаров")
            print("  python Script.py test-xml       - тестировать генерацию XML")
            print("  python Script.py upload-xml     - загрузить XML в Kaspi.kz")
            print("  python Script.py help          - показать помощь")
            print("  python Script.py               - полный запуск")
            return
    
    # Полный запуск (по умолчанию)
    logging.info("=== ПОЛНЫЙ ЗАПУСК СИСТЕМЫ ===")
    
    # Получаем список товаров из Al Style
    products = get_al_style_products()
    logging.info(f"Получено {len(products)} товаров из вашего интернет-магазина")

    # Обновляем цены и остатки в Kaspi.kz с валидацией
    xml_valid = update_kaspi_prices_stock(products)
    if xml_valid:
        logging.info("Цены и остатки обновлены на Kaspi.kz - XML валиден")
        
        # Загружаем XML файл в Kaspi.kz
        xml_uploaded = upload_xml_to_kaspi(config.xml_filename)
        if xml_uploaded:
            logging.info("XML файл успешно загружен в Kaspi.kz")
        else:
            logging.error("Ошибка при загрузке XML файла в Kaspi.kz")
    else:
        logging.error("Ошибка валидации XML - проверьте данные товаров")
        return  # Останавливаем выполнение при ошибке валидации

    # Обрабатываем заказы с Kaspi.kz
    process_kaspi_orders()
    logging.info("Обработка заказов с Kaspi.kz завершена")

if __name__ == "__main__":
    main()  # Запускаем программ
