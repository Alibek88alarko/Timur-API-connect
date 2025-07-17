#!/usr/bin/env python3
"""
Улучшенный генератор XML с дополнительными полями для Kaspi
"""
import json
import time
import logging
from xml.etree.ElementTree import Element, SubElement, tostring
import xml.dom.minidom
from Script import get_al_style_products
from config import config

def generate_enhanced_xml(products):
    """Генерирует улучшенный XML с дополнительными полями"""
    
    print("🔧 Создание улучшенного XML для Kaspi.kz")
    print("=" * 50)
    
    # Создаем корневой элемент
    kaspi_catalog = Element('kaspi_catalog', {
        'date': time.strftime('%Y-%m-%dT%H:%M:%S'),
        'xmlns': 'kaspiShopping',
        'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
        'xsi:schemaLocation': 'kaspiShopping http://kaspi.kz/kaspishopping.xsd'
    })
    
    # Компания
    company = SubElement(kaspi_catalog, 'company')
    company.text = config.company_name
    
    # ID продавца
    merchantid = SubElement(kaspi_catalog, 'merchantid')
    merchantid.text = config.merchant_id
    
    # Категории (добавляем базовые категории)
    categories = SubElement(kaspi_catalog, 'categories')
    
    # Основные категории для электроники
    category_mapping = {
        'Кабели': 'cables',
        'Клавиатуры': 'keyboards', 
        'Аксессуары': 'accessories',
        'Патч-корды': 'patch-cords',
        'Сетевое оборудование': 'network'
    }
    
    for cat_name, cat_id in category_mapping.items():
        category = SubElement(categories, 'category', {
            'id': cat_id,
            'parentId': 'electronics'
        })
        category.text = cat_name
    
    # Предложения
    offers = SubElement(kaspi_catalog, 'offers')
    
    processed_count = 0
    
    for product in products:
        try:
            # SKU - обязательное поле
            sku = str(product.get('article_pn') or product.get('article') or '').strip()
            if not sku:
                continue
                
            # Название товара
            name = product.get('name', '').strip()
            if not name:
                continue
                
            offer = SubElement(offers, 'offer', {
                'sku': sku,
                'available': 'true'
            })
            
            # Название
            model = SubElement(offer, 'model')
            model.text = name
            
            # Бренд
            brand = SubElement(offer, 'brand')
            brand.text = product.get('brand', 'No Brand').strip()
            
            # Категория (пытаемся определить автоматически)
            category_id = determine_category(name)
            categoryId = SubElement(offer, 'categoryId')
            categoryId.text = category_id
            
            # Цена
            price = SubElement(offer, 'price')
            price_value = product.get('price2') or product.get('price1') or '0'
            price.text = str(price_value)
            
            # Валюта
            currencyId = SubElement(offer, 'currencyId')
            currencyId.text = 'KZT'
            
            # Описание (важно для распознавания!)
            description = SubElement(offer, 'description')
            description.text = create_description(product)
            
            # Доступность
            availabilities = SubElement(offer, 'availabilities')
            quantity = get_stock_count(product.get('quantity'))
            
            availability = SubElement(availabilities, 'availability', {
                'available': 'yes' if int(quantity) > 0 else 'no',
                'storeId': config.store_id,
                'preOrder': '0',
                'stockCount': quantity
            })
            
            # Дополнительные параметры
            params = SubElement(offer, 'params')
            
            # Добавляем параметры
            add_param(params, 'Артикул', sku)
            add_param(params, 'Бренд', product.get('brand', 'No Brand'))
            
            # Если есть дополнительная информация
            if product.get('weight'):
                add_param(params, 'Вес', str(product.get('weight')))
            
            processed_count += 1
            
        except Exception as e:
            logging.error(f"Ошибка при обработке товара {sku}: {e}")
            continue
    
    # Форматируем XML
    rough_string = tostring(kaspi_catalog, encoding='utf-8')
    reparsed = xml.dom.minidom.parseString(rough_string)
    pretty_xml = reparsed.toprettyxml(indent="  ")
    
    # Сохраняем файл
    filename = f'kaspi_enhanced_{time.strftime("%Y%m%d_%H%M%S")}.xml'
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(pretty_xml)
    
    print(f"✅ Создан улучшенный XML: {filename}")
    print(f"📊 Обработано товаров: {processed_count}")
    
    return filename

def determine_category(name):
    """Определяет категорию товара по названию"""
    name_lower = name.lower()
    
    if 'клавиатура' in name_lower:
        return 'keyboards'
    elif 'кабель' in name_lower or 'патч' in name_lower:
        return 'cables'
    elif 'корд' in name_lower:
        return 'patch-cords'
    else:
        return 'accessories'

def create_description(product):
    """Создает подробное описание товара"""
    name = product.get('name', '')
    brand = product.get('brand', '')
    
    description = f"{name}"
    
    if brand and brand != 'Unknown':
        description += f" от {brand}"
    
    # Добавляем дополнительную информацию
    if product.get('price1'):
        description += f". Цена: {product.get('price1')} тенге"
    
    return description

def add_param(params_element, name, value):
    """Добавляет параметр в XML"""
    param = SubElement(params_element, 'param', {'name': name})
    param.text = str(value)

def get_stock_count(quantity):
    """Обрабатывает количество товара"""
    if isinstance(quantity, str):
        quantity = quantity.strip()
        if '>' in quantity:
            return '500'
        elif quantity.isdigit():
            return quantity
        else:
            return '0'
    elif isinstance(quantity, (int, float)):
        return str(int(quantity))
    else:
        return '0'

def main():
    """Основная функция"""
    print("🚀 Генерация улучшенного XML для Kaspi.kz")
    print("=" * 50)
    
    # Получаем товары
    products = get_al_style_products()
    
    if not products:
        print("❌ Не удалось получить товары")
        return
    
    # Генерируем XML
    xml_file = generate_enhanced_xml(products)
    
    print(f"\n✅ Готово!")
    print(f"📁 Файл: {xml_file}")
    print(f"📋 Инструкция:")
    print(f"  1. Загрузите файл {xml_file} в кабинет Kaspi")
    print(f"  2. Если товары все еще 'нераспознанные' - нужно изучить требования")
    print(f"  3. Обратитесь в техподдержку Kaspi: 2323")

if __name__ == "__main__":
    main()
