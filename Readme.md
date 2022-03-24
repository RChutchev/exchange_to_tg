# Почта из OWA Exchange в telegramm (только непрочитанные сообщения)

## Установка
- git clone https://github.com/twmd/exchange_to_tg
- pip install -r requirements.txt

## Настройка
1. Переименовываем фаил setting_example.ini  в setting.ini
2. В файле setting.ini описаны следующие опции
- [OWA] - Раздел подключения к серверу OWA
- username = - Имя пользователя в формате домен\имя пользователя
- password = - Пароль
- server =   - Имя сервера пример owa.test.com

- [TG] - Раздел подключения к telegramm
- token = - Токен дота телеграмм
- group_id = - ID группы куда бот будет слать сообщения

## Логирование
По умолчанию логирование включенно в режиме debug, для изменения этого необходимо в файле logger.ini в разделе [logger_plogger]
level=DEBUG, заменить DEBUG на CRITICAL