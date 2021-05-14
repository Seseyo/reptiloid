# -*- coding: utf-8 -*-
"""
Created on Tue May 11 13:59:25 2021

@author: chapaeva
"""

import telebot
import bs4
import parser
import urllib.request
from bs4 import BeautifulSoup

#main variables
TOKEN = "1892250089:AAFqSOmIBfTvFYanFrFUVx8KKksCVpvEqxs"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'go'])
def start_handler(message):
#    global isRunning
#    if not isRunning:
        chat_id = message.chat.id
        text = message.text
        msg = bot.send_message(chat_id, 'Сколько вам лет?')
        bot.register_next_step_handler(msg, askAge)
        isRunning = True
    
def askAge(message):
    chat_id = message.chat.id
    text = message.text
    if not text.isdigit():
        msg = bot.send_message(chat_id, 'Возраст должен быть числом, введите ещё раз.')
        bot.register_next_step_handler(msg, askAge) #askSource
        return
    msg = bot.send_message(chat_id, 'Спасибо, я запомнил что вам ' + text + ' лет.')
#    isRunning = False
    
@bot.message_handler(content_types=['photo'])
def text_handler(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Красиво.')
    
#parser
def getTitlesFromAll(amount, rating='all'):
    output = ''
    for i in range(1, amount+1):
        try:
            if rating == 'all':
                html = urllib.request.urlopen('https://habrahabr.ru/all/page'+ str(i) +'/').read()
            else:
                html = urllib.request.urlopen('https://habrahabr.ru/all/'+ rating +'/page'+ str(i) +'/').read()
        except urllib.error.HTTPError:
            print('Error 404 Not Found')
            break
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.find_all('a', class_ = 'post__title_link')
        for i in title:
            i = i.get_text()
            output += ('- "'+i+'",\n')
    return output

def getTitlesFromTop(amount, age='daily'):
    output = ''
    for i in range(1, amount+1):
        try:
            html = urllib.request.urlopen('https://habrahabr.ru/top/'+ age +'/page'+ str(i) +'/').read()
        except urllib.error.HTTPError:
            print('Error 404 Not Found')
            break
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.find_all('a', class_ = 'post__title_link')
        for i in title:
            i = i.get_text()
            output += ('- "'+i+'",\n')
    return output
"""
@bot.message_handler(content_types=['text'])
def text_handler(message):
    text = message.text.lower()
    chat_id = message.chat.id
    if text == "привет":
        bot.send_message(chat_id, 'Привет, я бот - парсер хабра.')
    elif text == "как дела?":
        bot.send_message(chat_id, 'Хорошо, а у тебя?')
    else:
        bot.send_message(chat_id, 'Простите, я вас не понял :(')
"""       
bot.polling()