"""
Конфигурация приложения
Загружает настройки из переменных окружения
"""

import os
from dataclasses import dataclass
from dotenv import load_dotenv

# Загружаем переменные из .env файла
load_dotenv()

@dataclass
class Config:
    """Класс конфигурации приложения"""
    
    # API токены
    al_style_token: str = os.getenv('AL_STYLE_TOKEN', '')
    kaspi_token: str = os.getenv('KASPI_TOKEN', '')
    
    # API URLs
    al_style_api_url: str = os.getenv('AL_STYLE_API_URL', 'https://api.al-style.kz/api')
    kaspi_api_url: str = os.getenv('KASPI_API_URL', 'https://kaspi.kz/shop/api/v2')
    
    # Настройки запросов
    request_delay: int = int(os.getenv('REQUEST_DELAY', '5'))
    
    # Kaspi настройки
    store_id: str = os.getenv('STORE_ID', 'myFavoritePickupPoint1')
    merchant_id: str = os.getenv('MERCHANT_ID', '01')
    company_name: str = os.getenv('COMPANY_NAME', 'Al-Style')
    
    # Файлы
    xml_filename: str = 'kaspi_price_list.xml'
    
    def validate(self) -> bool:
        """Проверяет, что все обязательные настройки заданы"""
        if not self.al_style_token:
            raise ValueError("AL_STYLE_TOKEN не установлен")
        if not self.kaspi_token:
            raise ValueError("KASPI_TOKEN не установлен")
        return True

# Глобальный экземпляр конфигурации
config = Config()

# Заголовки для API запросов
AL_STYLE_HEADERS = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

KASPI_HEADERS = {
    'Content-Type': 'application/vnd.api+json',
    'X-Auth-Token': config.kaspi_token
}
