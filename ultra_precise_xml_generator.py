#!/usr/bin/env python3
"""
Ультра-точный генератор XML на основе оригинального kaspi_price_list.xml
"""
import json
import time
import logging
from xml.etree.ElementTree import Element, SubElement, tostring
import xml.dom.minidom
from Script import get_al_style_products
from config import config

def generate_ultra_precise_xml(products):
    """Генерирует XML точно по образцу оригинального kaspi_price_list.xml"""
    
    print("🎯 Создание XML точно по образцу оригинального файла")
    print("=" * 50)
    
    # Создаем корневой элемент ТОЧНО как в оригинале
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
    
    # Offers
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
                'sku': sku
            })
            
            # ТОЧНО как в оригинале:
            # 1. model
            model = SubElement(offer, 'model')
            model.text = name
            
            # 2. brand
            brand = SubElement(offer, 'brand')
            brand.text = product.get('brand', 'Unknown').strip()
            
            # 3. availabilities (ТОЧНО как в оригинале)
            availabilities = SubElement(offer, 'availabilities')
            quantity = get_stock_count(product.get('quantity'))
            
            # Элемент availability с теми же атрибутами что в оригинале
            availability = SubElement(availabilities, 'availability', {
                'available': 'yes' if int(quantity) > 0 else 'no',
                'storeId': config.store_id,
                'preOrder': '0',
                'stockCount': quantity
            })
            
            # 4. price (ТОЧНО как в оригинале)
            price = SubElement(offer, 'price')
            price_value = product.get('price2') or product.get('price1') or '0'
            price.text = str(price_value)
            
            processed_count += 1
            
        except Exception as e:
            logging.error(f"Ошибка при обработке товара {sku}: {e}")
            continue
    
    # Сохраняем БЕЗ XML декларации (как в оригинале)
    rough_string = tostring(kaspi_catalog, encoding='unicode')
    
    # Добавляем XML декларацию вручную
    xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n' + rough_string
    
    # Сохраняем файл
    filename = f'kaspi_ultra_precise_{time.strftime("%Y%m%d_%H%M%S")}.xml'
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(xml_content)
    
    print(f"✅ Создан ультра-точный XML: {filename}")
    print(f"📊 Обработано товаров: {processed_count}")
    print(f"🎯 Точно повторяет структуру оригинального файла")
    
    return filename

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
    print("🎯 Генерация УЛЬТРА-ТОЧНОГО XML для Kaspi.kz")
    print("=" * 50)
    print("🔧 Копируем структуру оригинального kaspi_price_list.xml")
    print("=" * 50)
    
    # Получаем товары
    products = get_al_style_products()
    
    if not products:
        print("❌ Не удалось получить товары")
        return
    
    # Генерируем XML
    xml_file = generate_ultra_precise_xml(products)
    
    print(f"\n✅ Готово!")
    print(f"📁 Файл: {xml_file}")
    print(f"📋 Особенности:")
    print(f"  - Точная копия структуры оригинального файла")
    print(f"  - Тот же порядок элементов")
    print(f"  - Те же атрибуты")
    print(f"  - Та же кодировка")
    print(f"\n🎯 Следующие шаги:")
    print(f"  1. Загрузите файл {xml_file} в кабинет Kaspi")
    print(f"  2. Должно пройти валидацию без ошибок")
    print(f"  3. Ожидается: 'Всего товаров: {len(products)}'")

if __name__ == "__main__":
    main()
