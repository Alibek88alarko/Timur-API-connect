#!/usr/bin/env python3
"""
Система для автоматической загрузки товаров в Kaspi.kz с учетом лимитов
"""
import time
import datetime
import schedule
import logging
from Script import get_al_style_products, update_kaspi_prices_stock
from config import config

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('kaspi_auto_upload.log'),
        logging.StreamHandler()
    ]
)

class KaspiAutoUploader:
    def __init__(self):
        self.last_upload_time = None
        self.upload_limit_reset_time = None
        
    def check_upload_availability(self):
        """Проверяет, можно ли загружать товары"""
        current_time = datetime.datetime.now()
        
        if self.upload_limit_reset_time:
            if current_time < self.upload_limit_reset_time:
                time_left = self.upload_limit_reset_time - current_time
                logging.info(f"⏰ Лимит активен. Ожидание до {self.upload_limit_reset_time.strftime('%H:%M')}")
                logging.info(f"⏳ Осталось: {time_left}")
                return False
        
        return True
    
    def set_upload_limit(self, reset_time_str):
        """Устанавливает время сброса лимита"""
        today = datetime.date.today()
        try:
            reset_time = datetime.datetime.strptime(f"{today} {reset_time_str}", "%Y-%m-%d %H:%M")
            if reset_time < datetime.datetime.now():
                # Если время уже прошло, добавляем день
                reset_time += datetime.timedelta(days=1)
            
            self.upload_limit_reset_time = reset_time
            logging.info(f"🕐 Лимит установлен до: {reset_time.strftime('%Y-%m-%d %H:%M')}")
        except ValueError:
            logging.error(f"❌ Неверный формат времени: {reset_time_str}")
    
    def upload_products(self):
        """Загружает товары в Kaspi.kz"""
        if not self.check_upload_availability():
            return False
        
        try:
            logging.info("🚀 Начинаем загрузку товаров в Kaspi.kz")
            
            # Получаем актуальные товары
            products = get_al_style_products()
            if not products:
                logging.error("❌ Не удалось получить товары из Al-Style")
                return False
            
            logging.info(f"📦 Получено {len(products)} товаров")
            
            # Генерируем и загружаем XML
            result = update_kaspi_prices_stock()
            
            if result:
                self.last_upload_time = datetime.datetime.now()
                logging.info(f"✅ Успешная загрузка в {self.last_upload_time.strftime('%H:%M')}")
                return True
            else:
                logging.error("❌ Ошибка при загрузке")
                return False
                
        except Exception as e:
            logging.error(f"❌ Ошибка при загрузке: {e}")
            return False
    
    def schedule_upload(self, time_str):
        """Планирует загрузку на определенное время"""
        logging.info(f"📅 Планирование загрузки на {time_str}")
        schedule.every().day.at(time_str).do(self.upload_products)
    
    def run_scheduler(self):
        """Запускает планировщик"""
        logging.info("🔄 Запуск планировщика загрузок")
        logging.info("📋 Запланированные задачи:")
        for job in schedule.jobs:
            logging.info(f"  - {job}")
        
        while True:
            schedule.run_pending()
            time.sleep(60)  # Проверяем каждую минуту

def main():
    """Основная функция"""
    print("🤖 Система автоматической загрузки товаров в Kaspi.kz")
    print("=" * 60)
    
    uploader = KaspiAutoUploader()
    
    # Устанавливаем лимит до 21:43 (как показано в сообщении)
    uploader.set_upload_limit("21:43")
    
    # Планируем загрузку каждый день в 21:45 (после сброса лимита)
    uploader.schedule_upload("21:45")
    
    # Дополнительные загрузки
    uploader.schedule_upload("09:00")  # Утренняя загрузка
    uploader.schedule_upload("15:00")  # Дневная загрузка
    
    print("📅 Запланированные загрузки:")
    print("  - 09:00 - Утренняя синхронизация")
    print("  - 15:00 - Дневная синхронизация") 
    print("  - 21:45 - Вечерняя загрузка (после сброса лимита)")
    print("")
    print("🔄 Для остановки нажмите Ctrl+C")
    print("=" * 60)
    
    try:
        # Пробуем загрузить сейчас
        if uploader.check_upload_availability():
            print("🚀 Попытка загрузки сейчас...")
            uploader.upload_products()
        
        # Запускаем планировщик
        uploader.run_scheduler()
        
    except KeyboardInterrupt:
        logging.info("⏹️ Остановка планировщика")
        print("\n⏹️ Планировщик остановлен")

if __name__ == "__main__":
    main()
