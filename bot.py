#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import apiai, json
updater = Updater(token='485189131:AAEMhDY3es5sKDA4cwm8qFCqGEI3VZSTWq0') 
dispatcher = updater.dispatcher
# Обработка команд
def startCommand(bot, update):
    custom_keyboard = [['Как связаться с Сергеем?', 'У меня рабочие вопросы'], 
                       ['Просто поболтать']] 
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
    bot.send_message(chat_id=update.message.chat_id, text='Привет, давай пообщаемся?', reply_markup = reply_markup)
def textMessage(bot, update):
    request = apiai.ApiAI('d5092c43685245db9f5f5860cc2c4b39').text_request() # Токен API к Dialogflow
    request.lang = 'ru' # На каком языке будет послан запрос
    request.session_id = 'BatlabAIBot' # ID Сессии диалога (нужно, чтобы потом учить бота)
    if (update.message.text == 'Как связаться с Сергеем?'):
        bot.send_message(chat_id=update.message.chat_id, text='Лучше всего написать ему в телеграм @serega40in, там он, вероятно, Вам быстрее ответит')
    else:
        if (update.message.text == 'У меня рабочие вопросы'):
            custom_keyboard = [['Сколько стоят услуги по созданию сайтов?', 'А можно мне создать бота?'], 
                           ['Чем вообще занимается Сергей Сорокин и кто это такой??', 'Убери меню']] 
            reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
            bot.send_message(chat_id=update.message.chat_id, text='Да, да, Я вас слушаю.', reply_markup = reply_markup)
        else:
            if (update.message.text == 'Просто поболтать'):
                reply_markup = telegram.ReplyKeyboardRemove()
                bot.send_message(chat_id=update.message.chat_id, text='С удовольствием. Ведь имено простое общение меня развивает быстрее всего другого!', reply_markup=reply_markup)
            else:
                if (update.message.text == 'Сколько стоят услуги по созданию сайтов?'):
                    bot.send_message(chat_id=update.message.chat_id, text='Создание сайтов начинается от 5000 руб, за более точной информацией обращайтесь к Сергею @serega40in',)
                else:
                    if (update.message.text == 'А можно мне создать бота?'):
                        bot.send_message(chat_id=update.message.chat_id, text='Конечно! Я сам еще не умею создавать других ботиков, но если Вы обратитесь к Сергею: @serega40in, то он с удовольствием вам поможет',)
                    else:
                        if (update.message.text == 'Убери меню'):
                            reply_markup = telegram.ReplyKeyboardRemove()
                            bot.send_message(chat_id=update.message.chat_id, text='Сделано!', reply_markup=reply_markup)
                            bot.send_message(chat_id=update.message.chat_id, text='вот такой я исполнительный')
                        else:
                            if (update.message.text == 'Чем вообще занимается Сергей Сорокин и кто это такой??'):
                                bot.send_message(chat_id=update.message.chat_id, text='Подробнее узнать о Сергее Вы можете на сайте www.serega40in.ru')                            
                            else:
                                request.query = update.message.text # Посылаем запрос к ИИ с сообщением от юзера
                                responseJson = json.loads(request.getresponse().read().decode('utf-8'))
                                response = responseJson['result']['fulfillment']['speech'] # Разбираем JSON и вытаскиваем ответ
                                # Если есть ответ от бота - присылаем юзеру, если нет - бот его не понял
                                if response:
                                    bot.send_message(chat_id=update.message.chat_id, text=response)
                                else:
                                    bot.send_message(chat_id=update.message.chat_id, text='Я Вас не совсем понял!')
# Хендлеры
start_command_handler = CommandHandler('start', startCommand)
text_message_handler = MessageHandler(Filters.text, textMessage)
# Добавляем хендлеры в диспетчер
dispatcher.add_handler(start_command_handler)
dispatcher.add_handler(text_message_handler)
# Начинаем поиск обновлений
updater.start_polling(clean=True)
# Останавливаем бота, если были нажаты Ctrl + C
updater.idle()