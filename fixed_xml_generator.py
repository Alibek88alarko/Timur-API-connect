#!/usr/bin/env python3
"""
Исправленный генератор XML без категорий (только offers)
"""
import json
import time
import logging
from xml.etree.ElementTree import Element, SubElement, tostring
import xml.dom.minidom
from Script import get_al_style_products
from config import config

def generate_fixed_xml(products):
    """Генерирует исправленный XML только с offers"""
    
    print("🔧 Создание исправленного XML для Kaspi.kz")
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
    
    # ТОЛЬКО offers - БЕЗ categories!
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
            
            # Название
            model = SubElement(offer, 'model')
            model.text = name
            
            # Бренд
            brand = SubElement(offer, 'brand')
            brand.text = product.get('brand', 'Unknown').strip()
            
            # Цена
            price = SubElement(offer, 'price')
            price_value = product.get('price2') or product.get('price1') or '0'
            price.text = str(price_value)
            
            # Доступность
            availabilities = SubElement(offer, 'availabilities')
            quantity = get_stock_count(product.get('quantity'))
            
            availability = SubElement(availabilities, 'availability', {
                'available': 'yes' if int(quantity) > 0 else 'no',
                'storeId': config.store_id,
                'preOrder': '0',
                'stockCount': quantity
            })
            
            processed_count += 1
            
        except Exception as e:
            logging.error(f"Ошибка при обработке товара {sku}: {e}")
            continue
    
    # Форматируем XML
    rough_string = tostring(kaspi_catalog, encoding='utf-8')
    reparsed = xml.dom.minidom.parseString(rough_string)
    pretty_xml = reparsed.toprettyxml(indent="  ")
    
    # Сохраняем файл
    filename = f'kaspi_fixed_{time.strftime("%Y%m%d_%H%M%S")}.xml'
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(pretty_xml)
    
    print(f"✅ Создан исправленный XML: {filename}")
    print(f"📊 Обработано товаров: {processed_count}")
    print(f"🔧 Убрали categories - только offers!")
    
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
    print("🚀 Генерация ИСПРАВЛЕННОГО XML для Kaspi.kz")
    print("=" * 50)
    print("🔧 Исправлено: убрали categories - только offers")
    print("=" * 50)
    
    # Получаем товары
    products = get_al_style_products()
    
    if not products:
        print("❌ Не удалось получить товары")
        return
    
    # Генерируем XML
    xml_file = generate_fixed_xml(products)
    
    print(f"\n✅ Готово!")
    print(f"📁 Файл: {xml_file}")
    print(f"📋 Изменения:")
    print(f"  - Убрали <categories> элемент")
    print(f"  - Оставили только <offers>")
    print(f"  - Схема должна пройти валидацию")
    print(f"\n🎯 Следующие шаги:")
    print(f"  1. Загрузите файл {xml_file} в кабинет Kaspi")
    print(f"  2. Должно быть 'Всего товаров: {len(products)}'")
    print(f"  3. Если все равно ошибки - сообщите результат")

if __name__ == "__main__":
    main()
