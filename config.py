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
    
    # API URLs (правильные согласно официальной документации 2025)
    al_style_api_url: str = os.getenv('AL_STYLE_API_URL', 'https://api.al-style.kz/api')
    
    # Kaspi API - базовый URL (согласно документации Host: kaspi.kz)
    kaspi_base_url: str = 'https://kaspi.kz'
    kaspi_api_base: str = os.getenv('KASPI_API_URL', 'https://kaspi.kz/shop/api/v2')
    
    # Kaspi API endpoints (правильные пути)
    kaspi_orders_url: str = f'{kaspi_base_url}/shop/api/v2/orders'
    kaspi_products_url: str = f'{kaspi_base_url}/shop/api/v2/products'
    kaspi_xml_upload_url: str = f'{kaspi_base_url}/shop/api/v2/product/import'
    
    # Настройки запросов (с timeout)
    request_delay: int = int(os.getenv('REQUEST_DELAY', '5'))
    request_timeout: int = int(os.getenv('REQUEST_TIMEOUT', '30'))  # 30 сек для Kaspi API
    max_retries: int = int(os.getenv('MAX_RETRIES', '3'))
    
    # User-Agent для запросов (КРИТИЧНО для Kaspi API!)
    user_agent: str = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    
    # Kaspi pagination (ОБЯЗАТЕЛЬНЫЕ параметры согласно документации!)
    kaspi_page_size: int = 20  # Количество заказов на странице (макс. 100)
    kaspi_date_range_days: int = 14  # Максимальный диапазон дат для фильтра (макс. 14 дней!)
    
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
    'User-Agent': config.user_agent,  # КРИТИЧНО! Без User-Agent = timeout
    'Content-Type': 'application/vnd.api+json',
    'Accept': 'application/vnd.api+json',
    'X-Auth-Token': config.kaspi_token
}
