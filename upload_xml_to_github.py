#!/usr/bin/env python3
"""
Автоматическая публикация XML прайс-листа на GitHub
Создает публичный URL для автозагрузки в Kaspi.kz
"""
import os
import time
import logging
from pathlib import Path

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def upload_xml_to_github():
    """
    Загружает XML файл в репозиторий GitHub для публичного доступа
    """
    xml_file = 'kaspi_price_list.xml'
    
    if not os.path.exists(xml_file):
        logging.error(f"❌ Файл {xml_file} не найден!")
        return False
    
    try:
        logging.info("📤 Загрузка XML в GitHub...")
        
        # Добавляем файл в Git
        os.system('git add kaspi_price_list.xml')
        
        # Создаем коммит с текущей датой
        commit_message = f"Update price list {time.strftime('%Y-%m-%d %H:%M:%S')}"
        os.system(f'git commit -m "{commit_message}"')
        
        # Отправляем в GitHub
        os.system('git push origin main')
        
        logging.info("✅ XML успешно загружен в GitHub!")
        logging.info("🌐 Публичный URL будет доступен через несколько минут")
        
        return True
        
    except Exception as e:
        logging.error(f"❌ Ошибка при загрузке: {e}")
        return False

def get_github_xml_url():
    """
    Возвращает публичный URL для XML файла на GitHub
    """
    # URL формируется как: https://raw.githubusercontent.com/ВАШ_USERNAME/ВАШ_РЕПО/main/kaspi_price_list.xml
    repo_owner = "Alibek88alarko"  # Из вашего репозитория
    repo_name = "Timur-API-connect"
    branch = "main"
    filename = "kaspi_price_list.xml"
    
    url = f"https://raw.githubusercontent.com/{repo_owner}/{repo_name}/{branch}/{filename}"
    
    logging.info(f"📋 Публичный URL для Kaspi.kz:")
    logging.info(f"   {url}")
    
    return url

if __name__ == "__main__":
    print("=" * 70)
    print("🚀 ПУБЛИКАЦИЯ XML ПРАЙС-ЛИСТА НА GITHUB")
    print("=" * 70)
    print()
    
    # Получаем URL
    url = get_github_xml_url()
    
    print("\n📝 ИНСТРУКЦИЯ:")
    print("1. Запустите этот скрипт после генерации XML")
    print("2. Скопируйте URL выше")
    print("3. Вставьте в Kaspi кабинет → Автоматическая загрузка")
    print()
    
    response = input("Загрузить XML в GitHub сейчас? (y/n): ")
    
    if response.lower() == 'y':
        if upload_xml_to_github():
            print(f"\n✅ Готово! Используйте этот URL в Kaspi:")
            print(f"   {url}")
        else:
            print("\n❌ Не удалось загрузить XML")
    else:
        print("\n⏹️ Отменено")
