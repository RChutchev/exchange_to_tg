#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os.path

from exchangelib import Credentials, Account, DELEGATE, Configuration
import logging
import logging.config
import configparser
import telebot

config_path = os.path.join(os.getcwd(), 'setting.ini')


# Логирование
def get_logger():
    logging.config.fileConfig(os.path.join(os.getcwd(), 'logger.ini'), disable_existing_loggers=False)
    logger = logging.getLogger('plogger')
    return logger


logger = get_logger()


def get_config(config_path: str, section: str) -> dict:
    """
    Получаем конфиг
    :param config_path: путь до файла конфигурации
    :param section: имя секции
    :return: возвращает словарь из options указанной секции
    """
    config = configparser.ConfigParser()
    try:
        config.read(config_path)
    except Exception as e:
        logger.error('Чтение файла конфигурации')
    logger.info('Фаил конфигурации прочитан')
    return dict(config.items(section))


# Подключение к серверу
def connection(username: str, password: str, server: str, email):
    credentials = Credentials(username=username, password=password)
    config = Configuration(server=server, credentials=credentials)
    return Account(
        primary_smtp_address=email,
        config=config,
        autodiscover=False,
        access_type=DELEGATE,
    )


if __name__ == "__main__":
    owa_config_dict = {}
    tg_config_dict = {}
    try:
        owa_config_dict = get_config(config_path, 'OWA')
        tg_config_dict = get_config(config_path, 'TG')
    except Exception as e:
        logger.error('Получение параметров конфигурации')
    try:
        acc = connection(owa_config_dict['username'], owa_config_dict['password'], owa_config_dict['server'],
                         owa_config_dict['email'])
    except Exception as e:
        logger.error('Подключение к Exchange')
    else:
        logger.info('Подключение к серверу состоялось')
        bot = telebot.TeleBot(token=tg_config_dict['token'])
        for item in acc.inbox.all().filter(is_read=False).only('subject', 'text_body'):
            subject = item.subject
            body = item.text_body
            try:
                bot.send_message(tg_config_dict['group_id'], subject + '\n' + body)
            except Exception as e:
                logger.error('Отправка сообщений в телеграмм состоялась.')
            item.is_read = True
            item.save(update_fields=['is_read'])
        else:
            logger.info('Новых сообщений не было')
