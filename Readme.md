# Почта из OWA Exchange в telegram (только непрочитанные сообщения из inbox)

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
- email = email пользователя

- [TG] - Раздел подключения к telegramm
- token = - Токен дота телеграмм
- group_id = - ID группы куда бот будет слать сообщения

## Запуск
- Для запуска необходим python версии 3.6 или выше.
- Если запускатся из python файла в ОС Windows, то необходимо создать рядом в директории .bat фаил с содержанием "python3 ext_to_tg.py"


## Логирование
По умолчанию логирование включенно в режиме debug, для изменения этого необходимо в файле logger.ini в разделе [logger_plogger]
level=DEBUG, заменить DEBUG на ERROR

