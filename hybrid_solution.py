#!/usr/bin/env python3
"""
Гибридное решение: автоматическая генерация XML + инструкция для ручной загрузки
"""
import os
import time
import shutil
from datetime import datetime
from pathlib import Path

def create_hybrid_solution():
    """Создает XML файлы для ручной загрузки с инструкциями"""
    
    print("🔄 Гибридное решение: Автоматическая генерация + ручная загрузка")
    print("=" * 70)
    
    # Создаем папку для готовых файлов
    upload_folder = Path("ready_for_upload")
    upload_folder.mkdir(exist_ok=True)
    
    # Импортируем нашу функцию генерации XML
    import sys
    sys.path.append('.')
    from Script import get_al_style_products, update_kaspi_prices_stock
    
    print("📦 Получение товаров из Al-Style...")
    products = get_al_style_products()
    
    if not products:
        print("❌ Не удалось получить товары")
        return
    
    print(f"✅ Получено {len(products)} товаров")
    
    # Генерируем XML
    print("🔧 Генерация XML файла...")
    xml_valid = update_kaspi_prices_stock(products)
    
    if not xml_valid:
        print("❌ Ошибка при генерации XML")
        return
    
    # Создаем timestamp для уникального имени
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Копируем файл в папку для загрузки
    original_file = "kaspi_price_list.xml"
    new_filename = f"kaspi_upload_{timestamp}.xml"
    new_filepath = upload_folder / new_filename
    
    shutil.copy2(original_file, new_filepath)
    
    # Создаем инструкцию
    instruction_file = upload_folder / f"ИНСТРУКЦИЯ_{timestamp}.txt"
    
    instruction_text = f"""
🎯 ИНСТРУКЦИЯ ПО ЗАГРУЗКЕ ТОВАРОВ В KASPI.KZ

📅 Дата создания: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}
📦 Количество товаров: {len(products)}
📄 Файл для загрузки: {new_filename}

📋 ПОШАГОВАЯ ИНСТРУКЦИЯ:

1. 🌐 Откройте кабинет продавца Kaspi.kz
   https://kaspi.kz/merchantcabinet

2. 🔐 Авторизуйтесь в системе

3. 📂 Перейдите в раздел "Управление товарами"

4. 📤 Найдите кнопку "Выберите файл" или "Загрузить файл"

5. 📁 Выберите файл: {new_filename}

6. ✅ Нажмите "Загрузить" или "Отправить"

7. ⏳ Дождитесь обработки (может занять несколько минут)

8. 📊 Проверьте результат в разделе товаров

⚠️ ВАЖНО:
- Загружайте ТОЛЬКО этот файл: {new_filename}
- НЕ изменяйте содержимое файла
- Если возникли ошибки, проверьте формат данных

🔄 ДЛЯ СЛЕДУЮЩЕГО ОБНОВЛЕНИЯ:
- Запустите скрипт снова: python hybrid_solution.py
- Будет создан новый файл с актуальными данными

📞 ТЕХПОДДЕРЖКА:
- Kaspi.kz: 2323
- Проблемы с файлом: проверьте логи программы
"""
    
    with open(instruction_file, 'w', encoding='utf-8') as f:
        f.write(instruction_text)
    
    print(f"✅ Готово!")
    print(f"📁 Файлы созданы в папке: {upload_folder}")
    print(f"📄 XML файл: {new_filename}")
    print(f"📋 Инструкция: ИНСТРУКЦИЯ_{timestamp}.txt")
    
    # Показываем краткую инструкцию
    print("\n" + "="*50)
    print("🚀 БЫСТРАЯ ИНСТРУКЦИЯ:")
    print("1. Откройте кабинет продавца Kaspi.kz")
    print("2. Перейдите в 'Управление товарами'")
    print(f"3. Загрузите файл: {new_filename}")
    print("4. Дождитесь обработки")
    print("="*50)
    
    # Открываем папку в проводнике (Windows)
    if os.name == 'nt':  # Windows
        os.startfile(upload_folder)
    
    return new_filepath

if __name__ == "__main__":
    create_hybrid_solution()
