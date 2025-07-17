#!/usr/bin/env python3
"""
Скрипт для анализа цен в исходных данных из Al-Style API
"""
import json
from Script import get_al_style_products

def analyze_prices():
    """Анализирует цены в исходных данных"""
    print("🔍 Анализ цен в исходных данных Al-Style")
    print("=" * 60)
    
    # Получаем товары
    products = get_al_style_products()
    
    if not products:
        print("❌ Не удалось получить товары")
        return
    
    # Статистика
    total_products = len(products)
    price_stats = {
        'price1_zero': 0,
        'price2_zero': 0,
        'price1_one': 0,
        'price2_one': 0,
        'price1_empty': 0,
        'price2_empty': 0,
        'price1_normal': 0,
        'price2_normal': 0,
        'both_empty': 0
    }
    
    # Проблемные товары
    problematic_products = []
    
    print("📊 Анализ цен:")
    print("-" * 60)
    
    for i, product in enumerate(products[:10], 1):  # Первые 10 товаров для примера
        name = product.get('name', 'Без названия')[:50]
        price1 = product.get('price1')
        price2 = product.get('price2')
        article = product.get('article_pn') or product.get('article', 'Без артикула')
        
        print(f"{i:2d}. {name}")
        print(f"    Артикул: {article}")
        print(f"    price1: {price1} (тип: {type(price1)})")
        print(f"    price2: {price2} (тип: {type(price2)})")
        
        # Логика выбора цены как в коде
        final_price = price2 or price1 or '0'
        print(f"    Итоговая цена: {final_price}")
        
        # Проверяем на проблемные цены
        if final_price in ['0', '1', 0, 1]:
            problematic_products.append({
                'name': name,
                'article': article,
                'price1': price1,
                'price2': price2,
                'final_price': final_price
            })
            print(f"    ⚠️  ПРОБЛЕМНАЯ ЦЕНА!")
        
        print()
    
    # Полная статистика
    print("📈 Полная статистика цен:")
    print("-" * 60)
    
    for product in products:
        price1 = product.get('price1')
        price2 = product.get('price2')
        
        # Анализ price1
        if price1 is None or price1 == '':
            price_stats['price1_empty'] += 1
        elif str(price1) == '0':
            price_stats['price1_zero'] += 1
        elif str(price1) == '1':
            price_stats['price1_one'] += 1
        else:
            price_stats['price1_normal'] += 1
        
        # Анализ price2
        if price2 is None or price2 == '':
            price_stats['price2_empty'] += 1
        elif str(price2) == '0':
            price_stats['price2_zero'] += 1
        elif str(price2) == '1':
            price_stats['price2_one'] += 1
        else:
            price_stats['price2_normal'] += 1
        
        # Оба поля пустые
        if (price1 is None or price1 == '') and (price2 is None or price2 == ''):
            price_stats['both_empty'] += 1
        
        # Итоговая цена
        final_price = price2 or price1 or '0'
        if str(final_price) in ['0', '1']:
            problematic_products.append({
                'name': product.get('name', 'Без названия')[:50],
                'article': product.get('article_pn') or product.get('article', 'Без артикула'),
                'price1': price1,
                'price2': price2,
                'final_price': final_price
            })
    
    # Выводим статистику
    print(f"Всего товаров: {total_products}")
    print(f"")
    print(f"Price1 статистика:")
    print(f"  - Пустые: {price_stats['price1_empty']}")
    print(f"  - Нули: {price_stats['price1_zero']}")
    print(f"  - Единицы: {price_stats['price1_one']}")
    print(f"  - Нормальные: {price_stats['price1_normal']}")
    print(f"")
    print(f"Price2 статистика:")
    print(f"  - Пустые: {price_stats['price2_empty']}")
    print(f"  - Нули: {price_stats['price2_zero']}")
    print(f"  - Единицы: {price_stats['price2_one']}")
    print(f"  - Нормальные: {price_stats['price2_normal']}")
    print(f"")
    print(f"Оба поля пустые: {price_stats['both_empty']}")
    
    # Проблемные товары
    print(f"\n🚨 Проблемные товары (цена 0 или 1 тг): {len(problematic_products)}")
    print("-" * 60)
    
    for i, product in enumerate(problematic_products[:20], 1):  # Первые 20
        print(f"{i:2d}. {product['name']}")
        print(f"    Артикул: {product['article']}")
        print(f"    price1: {product['price1']}")
        print(f"    price2: {product['price2']}")
        print(f"    Итоговая цена: {product['final_price']} тг")
        print()
    
    if len(problematic_products) > 20:
        print(f"... и еще {len(problematic_products) - 20} товаров")
    
    # Сохраняем проблемные товары в файл
    if problematic_products:
        with open('problematic_prices.json', 'w', encoding='utf-8') as f:
            json.dump(problematic_products, f, ensure_ascii=False, indent=2)
        print(f"\n💾 Проблемные товары сохранены в problematic_prices.json")

if __name__ == "__main__":
    analyze_prices()
