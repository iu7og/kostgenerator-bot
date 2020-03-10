"""
      ===== KOSTGEN TELEGRAM BOT =====
      Copyright (C) 2020 IU7OG Team.

      Веселый Telegram-бот на основе библиотеки markovify.
"""

import telebot
from telebot import apihelper
import markovify
import multiprocessing
import schedule
import time

import bot.config as cfg
from random import choice

apihelper.proxy = {'https':cfg.PROXY}
print(cfg.PROXY)

rofl_db = []
bot = telebot.TeleBot(cfg.KOST_TOKEN)

with open("data/logs.txt", encoding="utf-8") as f:
    text = f.read()

text_model = markovify.NewlineText(text)


def schedule_message():
    """
        Запланированное сообщение.
    """

    # работать не будет
    for users in rofl_db:
        bot.send_message(user, generate_message())


def schedule_bot():
    """
        Планировщик сообщений.
    """

    schedule.every(300).minutes.do(schedule_message)

    while True:
        schedule.run_pending()
        time.sleep(1)


def generate_message():
    """
        Генерация сообщения.
    """

    return text_model.make_short_sentence(100)


@bot.message_handler(commands=["start"])
def authorization(message):
    """
        Приветствующее сообщение.
    """

    if message.chat.id not in rofl_db:
        bot.send_message(message.chat.id, cfg.START_MESSAGE)
        rofl_db.append(message.chat.id)
    else:
        bot.send_message(message.chat.id, choice(cfg.HATE_MESSAGES))


@bot.message_handler(commands=["help"])
def send_help(message):
    """
        Отправка с помощью студенту.
    """

    bot.send_message(message.chat.id, cfg.HELP_MESSAGE)


@bot.message_handler(func=lambda m: True)
def handle_messages(message):
    """
        Ответ фразой АК.
    """

    bot.send_message(message.chat.id, generate_message())


if __name__ == "__main__":
    multiprocessing.Process(target=schedule_bot, args=()).start()
    bot.polling()
