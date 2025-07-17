#!/usr/bin/env python3
"""
Тестирование функции обработки заказов из Kaspi
"""
from Script import process_kaspi_orders, test_kaspi_orders

def main():
    print("🧪 Тестирование обработки заказов из Kaspi.kz")
    print("=" * 50)
    
    print("📋 Что делает функция process_kaspi_orders():")
    print("1. Получает заказы со статусом APPROVED_BY_BANK")
    print("2. Принимает заказы (меняет статус на ACCEPTED_BY_MERCHANT)")
    print("3. Получает состав заказа (товары и количество)")
    print("4. Обновляет остатки в Al-Style API")
    print()
    
    print("🔍 Запуск тестирования...")
    print("=" * 50)
    
    try:
        # Тестируем разные статусы заказов
        test_kaspi_orders()
        print("\n" + "=" * 50)
        
        # Пробуем обработать заказы
        process_kaspi_orders()
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        print("\n💡 Возможные причины:")
        print("- Kaspi API недоступен (таймауты)")
        print("- Неправильный токен")
        print("- Нет заказов в статусе APPROVED_BY_BANK")
    
    print("\n🎯 Когда API заработает, функция будет:")
    print("✅ Автоматически обрабатывать заказы")
    print("✅ Обновлять остатки в Al-Style")
    print("✅ Менять статусы заказов в Kaspi")

if __name__ == "__main__":
    main()
