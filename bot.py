from aiogram import types
import telebot
import config
import requests
from bs4 import BeautifulSoup
from db_users import BotDB
import formatJSON

BotDB = BotDB('db')
bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def start(message: types.Message):
    if not BotDB.user_exists(message.from_user.id):
        BotDB.add_user(message.from_user.id)

    bot.send_message(message.chat.id, 'Добро пожаловать, этот бот создан для теста!\n'
                                      'Всего хорошего, досвидания!\n'
                                      'есть запросы:\n'
                                      '/help - помощь\n'
                                      '"/get_brand"+артикул товара\n'
                                      '"/get_title"+артикул товара\n'
                                      'например: /get_title 38567378')


@bot.message_handler(commands=['help'])
def help_0(message: types.Message):
    bot.send_message(message.chat.id, 'Есть запросы:\n'
                                      '"/get_brand"+артикул товара\n'
                                      '"/get_title"+артикул товара\n'
                                      'например: /get_title 38567378')
    BotDB.add_record(message.from_user.id, '/help', message.text)


@bot.message_handler(content_types=['text'])
def main(message):
    try:
        def get_html(text):
            formatJSON.format_JSON(text.split(' ')[1])
            r = requests.get("https://by.wildberries.ru/catalog/" + text.split(' ')[1] + "/detail.aspx?targetUrl=SP")
            soup = BeautifulSoup(r.content, 'html.parser')
            items = soup.find('h1', class_='same-part-kt__header')
            brand = items.find('span').string
            title = items.find_next('span').find_next('span').string
            if '/get_brand' in message.text:
                BotDB.add_record(message.from_user.id, brand, message.text)
                bot.send_message(message.chat.id, brand)
            elif '/get_title' in message.text:
                BotDB.add_record(message.from_user.id, title, message.text)
                bot.send_message(message.chat.id, title)

        if '/get_brand ' or '/get_title ' in message.text:
            get_html(message.text)
        else:
            bot.send_message(message.chat.id, 'Введите "/get_brand" или "/get_title" + артикул товара\n'
                                              '/help - помощь')
            BotDB.add_record(message.from_user.id, 'error(не верный запрос)', message.text)
    except:
        bot.send_message(message.chat.id,'сорри, нет ответа!\n'
                                         'Введите "/get_brand" или "/get_title" + артикул товара\n'
                                         '/help - помощь')
        BotDB.add_record(message.from_user.id, 'error(нету информации)', message.text)


if __name__ == '__main__':
    bot.polling(none_stop=True)
