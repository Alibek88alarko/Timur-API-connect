"""
XML Validator для проверки соответствия схеме Kaspi.kz
Модуль для валидации XML файлов прайс-листа против схемы kaspishopping.xsd
"""

import os
import logging
import requests
from lxml import etree
from typing import Tuple, Optional
import xml.etree.ElementTree as ET


class KaspiXMLValidator:
    """Класс для валидации XML файлов против схемы Kaspi.kz"""
    
    def __init__(self, schema_url: str = "http://kaspi.kz/kaspishopping.xsd"):
        """
        Инициализация валидатора
        
        Args:
            schema_url: URL схемы XSD для валидации
        """
        self.schema_url = schema_url
        self.schema = None
        self.logger = logging.getLogger(__name__)
        
    def download_schema(self) -> bool:
        """
        Загружает схему XSD с сайта Kaspi.kz
        
        Returns:
            bool: True если схема успешно загружена, False в противном случае
        """
        try:
            self.logger.info(f"Загрузка схемы с {self.schema_url}")
            response = requests.get(self.schema_url, timeout=30)
            response.raise_for_status()
            
            # Парсим схему
            schema_doc = etree.fromstring(response.content)
            self.schema = etree.XMLSchema(schema_doc)
            
            self.logger.info("Схема успешно загружена и разобрана")
            return True
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Ошибка при загрузке схемы: {e}")
            return False
        except etree.XMLSyntaxError as e:
            self.logger.error(f"Ошибка парсинга схемы: {e}")
            return False
        except Exception as e:
            self.logger.error(f"Неожиданная ошибка при загрузке схемы: {e}")
            return False
    
    def validate_xml_string(self, xml_content: str) -> Tuple[bool, str]:
        """
        Валидирует XML строку против схемы
        
        Args:
            xml_content: XML контент как строка
            
        Returns:
            Tuple[bool, str]: (валиден ли XML, сообщение об ошибке или успехе)
        """
        if not self.schema:
            if not self.download_schema():
                return False, "Не удалось загрузить схему для валидации"
        
        try:
            # Парсим XML
            xml_doc = etree.fromstring(xml_content.encode('utf-8'))
            
            # Валидируем против схемы
            if self.schema.validate(xml_doc):
                return True, "XML соответствует схеме Kaspi.kz"
            else:
                # Собираем все ошибки валидации
                errors = []
                for error in self.schema.error_log:
                    errors.append(f"Строка {error.line}: {error.message}")
                
                error_message = "Ошибки валидации:\n" + "\n".join(errors)
                return False, error_message
                
        except etree.XMLSyntaxError as e:
            return False, f"Ошибка синтаксиса XML: {e}"
        except Exception as e:
            return False, f"Неожиданная ошибка при валидации: {e}"
    
    def validate_xml_file(self, file_path: str) -> Tuple[bool, str]:
        """
        Валидирует XML файл против схемы
        
        Args:
            file_path: Путь к XML файлу
            
        Returns:
            Tuple[bool, str]: (валиден ли XML, сообщение об ошибке или успехе)
        """
        if not os.path.exists(file_path):
            return False, f"Файл не найден: {file_path}"
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                xml_content = file.read()
            
            return self.validate_xml_string(xml_content)
            
        except Exception as e:
            return False, f"Ошибка при чтении файла: {e}"
    
    def check_required_elements(self, xml_content: str) -> Tuple[bool, str]:
        """
        Проверяет наличие обязательных элементов в XML
        
        Args:
            xml_content: XML контент как строка
            
        Returns:
            Tuple[bool, str]: (все ли элементы присутствуют, сообщение)
        """
        try:
            root = ET.fromstring(xml_content)
            
            # Определяем пространство имен
            namespace = {'kaspi': 'kaspiShopping'}
            
            # Проверяем обязательные элементы
            company = root.find('.//kaspi:company', namespace)
            if company is None:
                company = root.find('.//company')
            
            merchantid = root.find('.//kaspi:merchantid', namespace)
            if merchantid is None:
                merchantid = root.find('.//merchantid')
            
            offers = root.find('.//kaspi:offers', namespace)
            if offers is None:
                offers = root.find('.//offers')
            
            required_elements = {
                'company': company,
                'merchantid': merchantid,
                'offers': offers
            }
            
            missing_elements = []
            for element_name, element in required_elements.items():
                if element is None:
                    missing_elements.append(element_name)
            
            if missing_elements:
                return False, f"Отсутствуют обязательные элементы: {', '.join(missing_elements)}"
            
            # Проверяем структуру предложений
            offers = root.find('.//offers')
            if offers is not None:
                for offer in offers.findall('offer'):
                    sku = offer.get('sku')
                    if not sku:
                        return False, "Найдено предложение без SKU"
                    
                    # Проверяем обязательные дочерние элементы
                    required_offer_elements = ['model', 'brand', 'price']
                    for req_elem in required_offer_elements:
                        if offer.find(req_elem) is None:
                            return False, f"В предложении {sku} отсутствует элемент {req_elem}"
            
            return True, "Все обязательные элементы присутствуют"
            
        except ET.ParseError as e:
            return False, f"Ошибка парсинга XML: {e}"
        except Exception as e:
            return False, f"Ошибка при проверке элементов: {e}"


def validate_kaspi_xml(file_path: str) -> None:
    """
    Функция для валидации XML файла Kaspi.kz
    
    Args:
        file_path: Путь к XML файлу для валидации
    """
    # Настраиваем логирование
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    validator = KaspiXMLValidator()
    
    print(f"🔍 Валидация файла: {file_path}")
    print("-" * 50)
    
    # Проверяем структуру
    print("1. Проверка структуры XML...")
    with open(file_path, 'r', encoding='utf-8') as f:
        xml_content = f.read()
    
    structure_valid, structure_message = validator.check_required_elements(xml_content)
    if structure_valid:
        print("✅ Структура XML корректна")
    else:
        print(f"❌ Ошибка структуры: {structure_message}")
        return
    
    # Валидируем против схемы
    print("\n2. Валидация против схемы Kaspi.kz...")
    schema_valid, schema_message = validator.validate_xml_file(file_path)
    
    if schema_valid:
        print("✅ XML соответствует схеме Kaspi.kz")
        print(f"📝 {schema_message}")
    else:
        print("❌ XML НЕ соответствует схеме")
        print(f"📝 {schema_message}")
    
    print("-" * 50)
    print(f"📊 Общий результат: {'ПРОЙДЕН' if structure_valid and schema_valid else 'НЕ ПРОЙДЕН'}")


if __name__ == "__main__":
    """Запуск валидации из командной строки"""
    import sys
    
    if len(sys.argv) != 2:
        print("Использование: python xml_validator.py <путь_к_xml_файлу>")
        print("Пример: python xml_validator.py kaspi_price_list.xml")
        sys.exit(1)
    
    xml_file_path = sys.argv[1]
    validate_kaspi_xml(xml_file_path)
