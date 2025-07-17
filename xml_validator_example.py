"""
Пример использования XML валидатора для Kaspi.kz
Демонстрирует различные способы валидации XML файлов
"""

from xml_validator import KaspiXMLValidator, validate_kaspi_xml
import logging

def example_usage():
    """Пример использования валидатора"""
    
    # Настраиваем логирование
    logging.basicConfig(level=logging.INFO)
    
    # Создаем экземпляр валидатора
    validator = KaspiXMLValidator()
    
    # Пример 1: Валидация существующего файла
    print("=== Пример 1: Валидация файла ===")
    xml_file = "kaspi_price_list.xml"
    
    valid, message = validator.validate_xml_file(xml_file)
    if valid:
        print(f"✅ Файл {xml_file} валиден: {message}")
    else:
        print(f"❌ Файл {xml_file} не валиден: {message}")
    
    # Пример 2: Проверка структуры
    print("\n=== Пример 2: Проверка структуры ===")
    with open(xml_file, 'r', encoding='utf-8') as f:
        xml_content = f.read()
    
    structure_ok, struct_message = validator.check_required_elements(xml_content)
    if structure_ok:
        print(f"✅ Структура корректна: {struct_message}")
    else:
        print(f"❌ Ошибка структуры: {struct_message}")
    
    # Пример 3: Использование удобной функции
    print("\n=== Пример 3: Полная валидация ===")
    validate_kaspi_xml(xml_file)

def create_test_xml():
    """Создает тестовый XML для демонстрации ошибок"""
    
    # Пример неправильного XML (без обязательных элементов)
    invalid_xml = """<?xml version="1.0" encoding="UTF-8"?>
<kaspi_catalog xmlns="kaspiShopping" date="2025-07-17T14:00:00">
    <!-- Отсутствует company и merchantid -->
    <offers>
        <offer sku="test123">
            <model>Test Product</model>
            <!-- Отсутствует brand и price -->
        </offer>
    </offers>
</kaspi_catalog>"""
    
    # Сохраняем тестовый XML
    with open("test_invalid.xml", 'w', encoding='utf-8') as f:
        f.write(invalid_xml)
    
    # Валидируем неправильный XML
    print("=== Тест неправильного XML ===")
    validator = KaspiXMLValidator()
    
    valid, message = validator.check_required_elements(invalid_xml)
    if not valid:
        print(f"❌ Найдены ошибки структуры: {message}")
    
    # Удаляем тестовый файл
    import os
    os.remove("test_invalid.xml")

if __name__ == "__main__":
    print("🔍 Демонстрация XML валидатора для Kaspi.kz")
    print("=" * 50)
    
    example_usage()
    
    print("\n" + "=" * 50)
    create_test_xml()
    
    print("\n📋 Возможности валидатора:")
    print("• Проверка структуры XML")
    print("• Валидация против схемы Kaspi.kz") 
    print("• Детальные сообщения об ошибках")
    print("• Проверка обязательных элементов")
    print("• Использование как модуль или standalone")
