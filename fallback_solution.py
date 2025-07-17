#!/usr/bin/env python3
"""
Обходное решение - работа только с Al-Style до исправления Kaspi API
"""
import requests
import json
import time
import logging
import os
from xml.etree.ElementTree import Element, SubElement, tostring
import xml.dom.minidom
from dotenv import load_dotenv

load_dotenv()

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'logs/api_fallback_{time.strftime("%Y%m%d")}.log'),
        logging.StreamHandler()
    ]
)

class APIFallback:
    """Класс для работы с API с обходными решениями"""
    
    def __init__(self):
        self.al_style_token = os.getenv('AL_STYLE_TOKEN')
        self.kaspi_token = os.getenv('KASPI_TOKEN')
        self.al_style_url = os.getenv('AL_STYLE_API_URL', 'https://api.al-style.kz/api')
        
    def get_al_style_products(self):
        """Получение товаров из Al-Style с обработкой ошибок"""
        logging.info('Получение товаров из Al-Style...')
        
        url = f"{self.al_style_url}/elements-pagination"
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        params = {
            'access-token': self.al_style_token,
            'limit': 100,
            'offset': 0,
            'additional_fields': 'brand,price1,price2,quantity,article_pn'
        }
        
        all_products = []
        
        try:
            while True:
                response = requests.get(url, headers=headers, params=params, timeout=30)
                
                if response.status_code != 200:
                    logging.error(f'Ошибка Al-Style API: {response.status_code}')
                    break
                
                data = response.json()
                products = data.get('elements', [])
                all_products.extend(products)
                
                logging.info(f'Получено {len(products)} товаров, всего: {len(all_products)}')
                
                pagination = data.get('pagination', {})
                if pagination.get('currentPage') >= pagination.get('totalPages'):
                    break
                
                params['offset'] += params['limit']
                time.sleep(2)  # Пауза между запросами
                
        except Exception as e:
            logging.error(f'Ошибка при получении товаров: {e}')
            
        return all_products
    
    def generate_xml_only(self, products):
        """Генерация XML файла для ручной загрузки"""
        logging.info('Генерация XML файла...')
        
        # Создаем XML структуру
        kaspi_catalog = Element('kaspi_catalog', {
            'date': time.strftime('%Y-%m-%dT%H:%M:%S'),
            'xmlns': 'kaspiShopping',
            'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
            'xsi:schemaLocation': 'kaspiShopping http://kaspi.kz/kaspishopping.xsd'
        })
        
        # Добавляем информацию о компании
        company = SubElement(kaspi_catalog, 'company')
        company.text = os.getenv('COMPANY_NAME', 'Al-Style')
        
        merchantid = SubElement(kaspi_catalog, 'merchantid')
        merchantid.text = os.getenv('MERCHANT_ID', '01')
        
        offers = SubElement(kaspi_catalog, 'offers')
        
        # Добавляем товары
        for product in products:
            sku = str(product.get('article_pn') or product.get('article') or '').strip()
            if not sku:
                continue
            
            offer = SubElement(offers, 'offer', {'sku': sku})
            
            # Модель
            model = SubElement(offer, 'model')
            model.text = product.get('name', 'No Name').strip()
            
            # Бренд
            brand = SubElement(offer, 'brand')
            brand.text = product.get('brand', 'Unknown').strip()
            
            # Доступность
            availabilities = SubElement(offer, 'availabilities')
            quantity = product.get('quantity', 0)
            stock_count = self._get_stock_count(quantity)
            
            availability = SubElement(availabilities, 'availability', {
                'available': 'yes' if int(stock_count) > 0 else 'no',
                'storeId': os.getenv('STORE_ID', 'myFavoritePickupPoint1'),
                'preOrder': '0',
                'stockCount': stock_count
            })
            
            # Цена
            price = SubElement(offer, 'price')
            price.text = str(product.get('price2') or product.get('price1') or '0')
        
        # Форматируем XML
        rough_string = tostring(kaspi_catalog, encoding='utf-8')
        reparsed = xml.dom.minidom.parseString(rough_string)
        pretty_xml = reparsed.toprettyxml(indent="  ")
        
        # Сохраняем файл
        filename = f'kaspi_price_list_{time.strftime("%Y%m%d_%H%M%S")}.xml'
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(pretty_xml)
        
        logging.info(f'XML файл сохранен: {filename}')
        return filename
    
    def _get_stock_count(self, quantity):
        """Обработка количества товара"""
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
    """Основная функция с обходным решением"""
    print("🚀 Запуск с обходным решением (только Al-Style)")
    print("=" * 50)
    
    # Создаем папку для логов
    os.makedirs('logs', exist_ok=True)
    
    fallback = APIFallback()
    
    # Получаем товары из Al-Style
    products = fallback.get_al_style_products()
    
    if not products:
        logging.error("Не удалось получить товары из Al-Style")
        return
    
    # Генерируем XML файл
    xml_file = fallback.generate_xml_only(products)
    
    print(f"\n✅ Успешно создан XML файл: {xml_file}")
    print(f"📊 Обработано товаров: {len(products)}")
    print("\n🔧 Следующие шаги:")
    print("1. Зайдите в личный кабинет Kaspi.kz")
    print("2. Загрузите XML файл вручную")
    print("3. Обратитесь в техподдержку Kaspi для исправления API")
    print("4. Проверьте настройки API в кабинете продавца")

if __name__ == "__main__":
    main()
