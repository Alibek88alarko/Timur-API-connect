# ПРОВЕРКА ТОКЕНА ЧЕРЕЗ CURL
# Если Python не работает, попробуем прямой HTTP запрос

## 🔧 КОМАНДЫ ДЛЯ POWERSHELL

### Тест 1: Простой GET запрос
```powershell
$headers = @{
    "X-Auth-Token" = "56Pj6wkGBX34/05TUMV1ptxrGCa1ZdMkderQA1+Gtr0="
    "Content-Type" = "application/vnd.api+json"
}

Invoke-WebRequest -Uri "https://kaspi.kz/shop/api/v2/orders?page[size]=1" -Headers $headers -Method GET -TimeoutSec 10
```

### Тест 2: С подробным выводом
```powershell
$headers = @{
    "X-Auth-Token" = "56Pj6wkGBX34/05TUMV1ptxrGCa1ZdMkderQA1+Gtr0="
}

try {
    $response = Invoke-WebRequest -Uri "https://kaspi.kz/shop/api/v2/orders" -Headers $headers -Method GET -TimeoutSec 10 -Verbose
    Write-Host "✅ Статус: $($response.StatusCode)"
    Write-Host "📄 Ответ: $($response.Content)"
} catch {
    Write-Host "❌ Ошибка: $($_.Exception.Message)"
    Write-Host "📋 StatusCode: $($_.Exception.Response.StatusCode.value__)"
}
```

### Тест 3: Проверка доступности (ping)
```powershell
Test-NetConnection -ComputerName kaspi.kz -Port 443 -InformationLevel Detailed
```

### Тест 4: Проверка через Invoke-RestMethod
```powershell
$headers = @{
    "X-Auth-Token" = "56Pj6wkGBX34/05TUMV1ptxrGCa1ZdMkderQA1+Gtr0="
    "Accept" = "application/vnd.api+json"
}

try {
    $result = Invoke-RestMethod -Uri "https://kaspi.kz/shop/api/v2/orders" -Headers $headers -Method GET -TimeoutSec 10
    Write-Host "✅ Успех!"
    $result | ConvertTo-Json -Depth 3
} catch {
    Write-Host "❌ Ошибка: $($_.Exception.Message)"
}
```

---

## 🔍 АЛЬТЕРНАТИВА: Использование curl (если установлен)

### Проверка наличия curl:
```powershell
curl --version
```

### Если curl есть:
```powershell
curl -X GET "https://kaspi.kz/shop/api/v2/orders?page[size]=1" `
  -H "Content-Type: application/vnd.api+json" `
  -H "X-Auth-Token: 56Pj6wkGBX34/05TUMV1ptxrGCa1ZdMkderQA1+Gtr0=" `
  -v `
  --max-time 10
```

---

## 📊 ЧТО ИСКАТЬ В РЕЗУЛЬТАТАХ:

### ✅ Хорошие признаки:
- `StatusCode: 200` - ВСЁ РАБОТАЕТ!
- `StatusCode: 401` - API работает, токен неверный
- `StatusCode: 403` - API работает, нет прав
- Любой ответ с заголовками от kaspi.kz

### ❌ Плохие признаки:
- `Timeout` - сервер не отвечает
- `Connection refused` - порт закрыт
- `SSL/TLS` ошибки - проблемы с сертификатом
- Нет ответа вообще

---

## 💡 ВОЗМОЖНЫЕ ПРОБЛЕМЫ:

### 1. Firewall блокирует запросы
```powershell
# Проверьте правила Windows Firewall
Get-NetFirewallRule | Where-Object {$_.DisplayName -like "*Python*"}
```

### 2. Антивирус блокирует
- Отключите антивирус на 5 минут
- Попробуйте запрос снова

### 3. Proxy/VPN
```powershell
# Проверьте настройки прокси
netsh winhttp show proxy
```

### 4. IP адрес заблокирован Kaspi
- Попробуйте с другого компьютера
- Попробуйте через мобильный интернет

---

## 🎯 СЛЕДУЮЩИЕ ШАГИ:

1. **Запустите Тест 2** (с try-catch) - увидите точную ошибку
2. Если timeout → проблема в сети/firewall/блокировке
3. Если 401/403 → проблема в токене
4. Если 200 → токен РАБОТАЕТ, проблема была в Python!

---

## 📞 ЧТО СПРОСИТЬ У ПОДДЕРЖКИ:

Если поддержка говорит "смотрите в интернете", спросите конкретно:

1. **"Какой endpoint использовать для получения заказов?"**
   - Ожидаемый ответ: https://kaspi.kz/shop/api/v2/orders

2. **"Какие заголовки нужны для авторизации?"**
   - Ожидаемый ответ: X-Auth-Token: ваш_токен

3. **"Как проверить, что API активирован?"**
   - Должны дать инструкцию или ссылку

4. **"Есть ли тестовый endpoint для проверки токена?"**
   - Может быть /api/v2/health или /api/v2/ping

5. **"Нужны ли дополнительные права/настройки кроме токена?"**
   - Может быть whitelist IP-адресов

---

## 🔗 ПОЛЕЗНЫЕ ССЫЛКИ:

- Документация: https://guide.kaspi.kz/partner/ru/shop/api/
- Кабинет: https://kaspi.kz/merchantcabinet/
- Поддержка: https://kaspi.kz/merchantcabinet/support
- Телефон: 2323
