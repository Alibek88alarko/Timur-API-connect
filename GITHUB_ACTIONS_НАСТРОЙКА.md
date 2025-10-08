# ⚙️ НАСТРОЙКА GITHUB ACTIONS ДЛЯ АВТОЗАГРУЗКИ

## 🎯 ЧТО ЭТО ДАЁТ?

GitHub Actions будет **автоматически**:
1. ✅ Получать товары из Al-Style
2. ✅ Генерировать XML прайс-лист
3. ✅ Публиковать XML на GitHub
4. ✅ Kaspi будет скачивать обновлённый XML каждые 60 минут

**Всё это БЕЗ вашего участия!** 🤖

---

## 📋 ПОШАГОВАЯ НАСТРОЙКА:

### **Шаг 1: Добавляем секреты в GitHub**

1. Откройте ваш репозиторий на GitHub:
   ```
   https://github.com/Alibek88alarko/Timur-API-connect
   ```

2. Перейдите: **Settings** → **Secrets and variables** → **Actions**

3. Нажмите **"New repository secret"**

4. Добавьте **первый секрет:**
   - **Name:** `AL_STYLE_TOKEN`
   - **Secret:** (вставьте ваш токен от Al-Style из файла `.env`)
   - Нажмите **"Add secret"**

5. Добавьте **второй секрет:**
   - **Name:** `KASPI_TOKEN`
   - **Secret:** (вставьте ваш токен от Kaspi: `56Pj6wkGBX34/05TUMV1ptxrGCa1ZdMkderQA1+Gtr0=`)
   - Нажмите **"Add secret"**

**Скриншот настройки:**
```
Settings → Secrets and variables → Actions

Repository secrets:
┌─────────────────────────────────────────┐
│ AL_STYLE_TOKEN     ••••••••••••••••••   │
│ KASPI_TOKEN        ••••••••••••••••••   │
└─────────────────────────────────────────┘
```

---

### **Шаг 2: Загружаем GitHub Actions workflow**

```powershell
# Добавляем созданный workflow файл в Git
git add .github/workflows/kaspi_auto_update.yml
git commit -m "Add GitHub Actions for auto price list update"
git push origin main
```

---

### **Шаг 3: Проверяем, что workflow работает**

1. Перейдите в репозиторий на GitHub

2. Откройте вкладку **"Actions"**

3. Вы увидите workflow **"Auto Update Kaspi Price List"**

4. Запустите вручную для теста:
   - Нажмите на workflow
   - Нажмите **"Run workflow"** → **"Run workflow"**

5. Дождитесь выполнения (1-2 минуты)

6. Проверьте, что `kaspi_price_list.xml` появился в репозитории

---

### **Шаг 4: Получаем публичный URL**

После успешного выполнения workflow, ваш XML будет доступен по адресу:

```
https://raw.githubusercontent.com/Alibek88alarko/Timur-API-connect/main/kaspi_price_list.xml
```

**Проверка:**
```powershell
# Откройте URL в браузере или PowerShell
curl https://raw.githubusercontent.com/Alibek88alarko/Timur-API-connect/main/kaspi_price_list.xml
```

Вы должны увидеть содержимое XML файла.

---

### **Шаг 5: Настраиваем Kaspi.kz**

1. Зайдите в **Кабинет продавца Kaspi.kz**

2. Перейдите: **Товары** → **Загрузить прайс-лист**

3. Выберите **"Автоматическая загрузка"** (как на вашем скриншоте)

4. Вставьте URL:
   ```
   https://raw.githubusercontent.com/Alibek88alarko/Timur-API-connect/main/kaspi_price_list.xml
   ```

5. **Логин и пароль:** Оставьте пустыми (не нужны)

6. Нажмите **"Сохранить"**

---

## ⏰ РАСПИСАНИЕ ОБНОВЛЕНИЙ:

GitHub Actions будет запускаться автоматически:

| Время (UTC+3) | Описание |
|---------------|----------|
| 09:00         | Утреннее обновление |
| 15:00         | Дневное обновление |
| 21:00         | Вечернее обновление |

**Kaspi проверяет URL каждые 60 минут**, поэтому товары будут обновляться в течение часа после генерации XML.

---

## 🔍 МОНИТОРИНГ:

### **Проверка статуса workflow:**

1. GitHub → Ваш репозиторий → Actions
2. Смотрите статус последнего запуска:
   - ✅ Зелёная галочка - всё ОК
   - ❌ Красный крестик - ошибка

### **Просмотр логов:**

1. Нажмите на нужный workflow run
2. Откройте job **"Update Kaspi Price List"**
3. Смотрите подробные логи каждого шага

### **Проверка обновления в Kaspi:**

1. Кабинет Kaspi → Товары → История загрузок
2. Смотрите, когда был загружен последний прайс-лист

---

## ❓ ЧАСТЫЕ ВОПРОСЫ:

### **Q: Workflow не запускается автоматически**
**A:** Проверьте, что:
- Секреты `AL_STYLE_TOKEN` и `KASPI_TOKEN` добавлены
- Файл `.github/workflows/kaspi_auto_update.yml` есть в репозитории
- В настройках репозитория Actions включены (Settings → Actions → General)

### **Q: Workflow падает с ошибкой**
**A:** Откройте логи workflow и проверьте:
- Шаг 4: Создание .env файла (токены должны быть правильные)
- Шаг 5: Генерация XML (должен успешно подключиться к Al-Style)

### **Q: XML не обновляется в Kaspi**
**A:** Проверьте:
- URL в настройках Kaspi правильный
- XML файл доступен по публичному URL (откройте в браузере)
- В Kaspi кабинете нет ошибок загрузки (История загрузок)

### **Q: Можно ли изменить расписание?**
**A:** Да! Отредактируйте файл `.github/workflows/kaspi_auto_update.yml`:
```yaml
schedule:
  - cron: '0 6 * * *'   # 9:00 UTC+3
  - cron: '0 12 * * *'  # 15:00 UTC+3
  - cron: '0 18 * * *'  # 21:00 UTC+3
```

Формат cron: `минута час день месяц день_недели`

**Примеры:**
- `'0 * * * *'` - каждый час
- `'*/30 * * * *'` - каждые 30 минут
- `'0 6,12,18 * * *'` - в 6:00, 12:00, 18:00 UTC

### **Q: Сколько стоит GitHub Actions?**
**A:** Для публичных репозиториев - **БЕСПЛАТНО!**
Для приватных - 2000 минут/месяц бесплатно (этого более чем достаточно)

---

## 🎯 ТЕСТИРОВАНИЕ:

### **Вариант 1: Ручной запуск workflow**

1. GitHub → Actions → Auto Update Kaspi Price List
2. Run workflow → Run workflow
3. Ждём 1-2 минуты
4. Проверяем, что XML обновился

### **Вариант 2: Локальный тест**

```powershell
# Генерируем XML локально
python Script.py test-xml

# Загружаем в GitHub
git add kaspi_price_list.xml
git commit -m "Test XML update"
git push origin main

# Проверяем доступность
curl https://raw.githubusercontent.com/Alibek88alarko/Timur-API-connect/main/kaspi_price_list.xml
```

---

## ✅ КОНТРОЛЬНЫЙ ЧЕКЛИСТ:

- [ ] Секреты `AL_STYLE_TOKEN` и `KASPI_TOKEN` добавлены в GitHub
- [ ] Файл `.github/workflows/kaspi_auto_update.yml` загружен в репозиторий
- [ ] Workflow запущен вручную и завершился успешно (✅)
- [ ] XML файл доступен по публичному URL
- [ ] URL добавлен в настройки Kaspi → Автоматическая загрузка
- [ ] В истории загрузок Kaspi появилась первая запись

---

## 🚀 ГОТОВО!

После настройки система будет работать **полностью автоматически**:

```
Каждый день в 9:00, 15:00, 21:00:
  ↓
GitHub Actions запускается
  ↓
Получает товары из Al-Style API
  ↓
Генерирует XML прайс-лист
  ↓
Публикует XML на GitHub
  ↓
Kaspi скачивает XML (каждые 60 минут)
  ↓
Товары обновлены! ✅
```

**Без вашего участия! Без сервера! Без статического IP!** 🎉
