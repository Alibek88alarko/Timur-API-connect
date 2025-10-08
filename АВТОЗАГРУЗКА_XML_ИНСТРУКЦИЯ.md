# 🚀 НАСТРОЙКА АВТОМАТИЧЕСКОЙ ЗАГРУЗКИ XML В KASPI.KZ

**Дата:** 8 октября 2025  
**Проблема:** XML генерируется локально, но Kaspi не может его скачать автоматически

---

## 🎯 РЕШЕНИЕ: GitHub Pages (БЕСПЛАТНО!)

### ✅ Преимущества:
- **Не нужен статический IP**
- **Не нужен сервер**
- **Бесплатно навсегда**
- **Постоянный публичный URL**
- **Работает 24/7**

---

## 📋 ПОШАГОВАЯ ИНСТРУКЦИЯ:

### **Шаг 1: Генерируем XML локально**

```powershell
# Генерируем актуальный прайс-лист
python Script.py test-xml
```

**Результат:** Файл `kaspi_price_list.xml` создан локально

---

### **Шаг 2: Публикуем XML на GitHub**

```powershell
# Загружаем XML в ваш репозиторий
python upload_xml_to_github.py
```

**Скрипт автоматически:**
1. Добавляет `kaspi_price_list.xml` в Git
2. Создает коммит
3. Отправляет в GitHub

---

### **Шаг 3: Получаем публичный URL**

Ваш XML будет доступен по адресу:

```
https://raw.githubusercontent.com/Alibek88alarko/Timur-API-connect/main/kaspi_price_list.xml
```

**Проверка доступности:**
```powershell
# Проверяем, что XML доступен публично
curl https://raw.githubusercontent.com/Alibek88alarko/Timur-API-connect/main/kaspi_price_list.xml
```

---

### **Шаг 4: Настраиваем Kaspi.kz**

1. Зайти в **Кабинет продавца Kaspi.kz**
2. Перейти: **Товары** → **Загрузить прайс-лист**
3. Выбрать: **"Автоматическая загрузка"**
4. Вставить URL:
   ```
   https://raw.githubusercontent.com/Alibek88alarko/Timur-API-connect/main/kaspi_price_list.xml
   ```
5. (Опционально) Указать логин/пароль (если нужна авторизация - в нашем случае НЕТ)
6. Нажать **"Сохранить"**

**Результат:** Kaspi будет автоматически скачивать ваш XML **каждые 60 минут**

---

## 🤖 АВТОМАТИЗАЦИЯ (Полная схема):

### **Вариант A: Локальный скрипт + GitHub Actions**

**1. Обновляем `kaspi_auto_uploader.py`:**

```python
def upload_products(self):
    """Загружает товары в Kaspi.kz"""
    try:
        logging.info("🚀 Начинаем загрузку товаров в Kaspi.kz")
        
        # Получаем актуальные товары
        products = get_al_style_products()
        
        # Генерируем XML
        result = update_kaspi_prices_stock(products)
        
        # Публикуем XML на GitHub
        if result:
            import os
            os.system('git add kaspi_price_list.xml')
            os.system(f'git commit -m "Auto update {time.strftime(\'%Y-%m-%d %H:%M\')}"')
            os.system('git push origin main')
            
            logging.info("✅ XML опубликован на GitHub")
            return True
    except Exception as e:
        logging.error(f"❌ Ошибка: {e}")
        return False
```

**2. Запускаем автозагрузчик:**

```powershell
# Запускаем с планировщиком (каждый день в 9:00, 15:00, 21:45)
python kaspi_auto_uploader.py
```

---

### **Вариант B: GitHub Actions (ВСЁ АВТОМАТИЧЕСКИ)**

**Создадим файл `.github/workflows/kaspi_auto_update.yml`:**

```yaml
name: Auto Update Kaspi Price List

on:
  schedule:
    - cron: '0 6,12,18 * * *'  # Каждый день в 9:00, 15:00, 21:00 (UTC+3)
  workflow_dispatch:  # Ручной запуск

jobs:
  update-prices:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v3
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      
      - name: Generate XML
        env:
          AL_STYLE_TOKEN: ${{ secrets.AL_STYLE_TOKEN }}
          KASPI_TOKEN: ${{ secrets.KASPI_TOKEN }}
        run: |
          python Script.py test-xml
      
      - name: Commit and push XML
        run: |
          git config --global user.name "Kaspi Bot"
          git config --global user.email "bot@kaspi.kz"
          git add kaspi_price_list.xml
          git commit -m "Auto update prices $(date '+%Y-%m-%d %H:%M:%S')" || echo "No changes"
          git push
```

**Настройка секретов в GitHub:**
1. Репозиторий → Settings → Secrets and variables → Actions
2. Добавить секреты:
   - `AL_STYLE_TOKEN` - ваш токен от Al-Style
   - `KASPI_TOKEN` - ваш токен от Kaspi

---

## 📊 СХЕМА РАБОТЫ:

```
┌─────────────────┐
│   Al-Style API  │  ← Получаем товары
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Script.py     │  ← Генерируем XML локально
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   GitHub Repo   │  ← Публикуем XML
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Kaspi.kz API   │  ← Скачивает XML каждые 60 минут
└─────────────────┘
```

---

## ⚙️ АЛЬТЕРНАТИВНЫЕ ВАРИАНТЫ:

### **Вариант 1: Google Drive / Dropbox**
- Загружаете XML на облако
- Делаете публичную ссылку
- Указываете в Kaspi

**Минусы:**
- ❌ Нужна ручная загрузка
- ❌ Ссылка может измениться

---

### **Вариант 2: Свой сервер (если есть)**
- Поднимаете простой HTTP сервер
- Делаете XML доступным по URL

**Пример на Python:**
```python
# simple_server.py
from http.server import HTTPServer, SimpleHTTPRequestHandler

class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/kaspi_price_list.xml':
            self.send_response(200)
            self.send_header('Content-type', 'application/xml')
            self.end_headers()
            with open('kaspi_price_list.xml', 'rb') as f:
                self.wfile.write(f.read())

httpd = HTTPServer(('', 8080), MyHandler)
httpd.serve_forever()
```

**Минусы:**
- ❌ Нужен постоянно работающий компьютер
- ❌ Нужно настроить роутер (проброс портов)
- ❌ Может понадобиться статический IP

---

### **Вариант 3: Платный хостинг**
- Любой дешевый хостинг (1-3$ в месяц)
- Загружаете XML по FTP/SFTP
- Получаете постоянный URL

**Минусы:**
- ❌ Платно
- ❌ Нужна ручная загрузка или настройка FTP

---

## 🎯 РЕКОМЕНДАЦИЯ:

### **НАЧНИТЕ С GITHUB PAGES:**

**Почему:**
1. ✅ Бесплатно
2. ✅ Не нужен статический IP
3. ✅ Постоянный URL
4. ✅ Простая интеграция с вашим репозиторием
5. ✅ GitHub Actions для автоматизации

**Как:**
```powershell
# 1. Генерируем XML
python Script.py test-xml

# 2. Публикуем на GitHub
python upload_xml_to_github.py

# 3. Копируем URL
https://raw.githubusercontent.com/Alibek88alarko/Timur-API-connect/main/kaspi_price_list.xml

# 4. Вставляем в Kaspi кабинет → Автоматическая загрузка
```

---

## ❓ ЧАСТЫЕ ВОПРОСЫ:

### **Q: Нужен ли мне статический IP?**
**A:** НЕТ, если используете GitHub Pages! Kaspi будет скачивать XML с GitHub.

### **Q: Сколько стоит GitHub Pages?**
**A:** Бесплатно для публичных репозиториев!

### **Q: Как часто Kaspi обновляет товары?**
**A:** Каждые **60 минут** автоматически

### **Q: Можно ли вручную запустить обновление?**
**A:** Да! В кабинете Kaspi есть кнопка "Загрузить сейчас"

### **Q: Что если забыл обновить XML?**
**A:** Настройте планировщик (kaspi_auto_uploader.py) или GitHub Actions

---

## 🚀 БЫСТРЫЙ СТАРТ:

```powershell
# 1. Генерируем XML
python Script.py test-xml

# 2. Публикуем на GitHub
git add kaspi_price_list.xml
git commit -m "Update price list"
git push origin main

# 3. Используем URL в Kaspi
https://raw.githubusercontent.com/Alibek88alarko/Timur-API-connect/main/kaspi_price_list.xml
```

**Готово!** ✅
