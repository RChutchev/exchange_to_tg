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
        logger.exception('Чтение файла конфигурации')
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
#Отсылка сообщения в телеграмм
def send_tg_msg(token, group_id, messages):
    #TODO: Перенести сюда сразу словарь конфигурации
    try:
        bot = telebot.TeleBot(token=token)
        bot.send_message(group_id, messages)
    except Exception as e:
        logger.exception('send_tg_msg Отсылка сообщений в телеграмм')
    else:
        logger.info('Сообщение в телеграм отправленно')

def get_unread_msg(config):
    try:
        acc = connection(config['username'], config['password'], config['server'],
                             config['email'])
    except Exception as e:
        logger.exception('get_unread_msg чтение сообщений почтового ящика')
    else:
        for item in acc.inbox.all().filter(is_read=False).only('subject', 'text_body'):
            subject = item.subject
            body = item.text_body
            send_tg_msg(tg_config_dict['token'], tg_config_dict['group_id'], subject + '\n' + body)
            item.is_read = True
            item.save(update_fields=['is_read'])
            logger.info('get_unread_msg отработала')

if __name__ == "__main__":
    try:
        owa_config_dict = get_config(config_path, 'OWA')
        tg_config_dict = get_config(config_path, 'TG')
    except Exception as e:
        logger.exception('Получение параметров конфигурации')
    else:
        get_unread_msg(owa_config_dict)
