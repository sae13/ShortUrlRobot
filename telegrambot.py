#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from datetime import datetime
import logging
from MyBotFatherToken import myBotFatherToken
import urllib.request
import urllib.parse
from random import random
welcome_text = "\
با سلام\
\n \
به تلگرام کوتاه کننده لینک خوش آمدید.\
\n \
http://t.me/shorturlrobot \
\n \
این پروژه اولین رباتی هست  که نوشتم و روی رسپبری پای من داره کار میکنه\
\n \
اگه خودتون هم دوست دارید باتتون رو راه اندازی کنید آموزش آدرس زیر رو ببینید \
\n \
https://t.me/WayIsee/49 \
\n \
با تشکر از ابراهیم پارسایی بابت سایت کوتاه کننده لینکشون \
برای استفاده از بات آدرس  سایت و لینک درخواستی رو بدید مثال: \
\n \
http://sae13.ir/archives/577 cpluslearning \
\n \
به شما آدرس کوتاه به صورت \
\n \
http://a4l.ir/cpluslearning \
\n \
میده. \
ارتباط با من: \
\n \
@saeb_m \
\n \
ارتباط با ابراهیم پارسایی: \
\n \
@SpiDeRBoY \
"
def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text=welcome_text)

def url(longurl, custom):
    url = "http://a4l.ir/shorten/"
    values = {'url' : longurl,
              'custom' : custom,
              }

    data = urllib.parse.urlencode(values)
    data = data.encode('ascii') # data should be bytes
    req = urllib.request.Request(url, data)
    with urllib.request.urlopen(req) as response:
       the_page = response.read()
    return the_page

def getCm(bot, update):
    userInfo = update.message.chat
    userMessage = update.message.text
    userMessageSplited = userMessage.split()
    if len(userMessageSplited) == 1:
        rand = list.str(random())
        randNum = ''.join(rand[3:9])
        userMessageSplited.append(randNum)
    longurl_data = userMessageSplited[0]
    custom_link = userMessageSplited[1]
    req = url(longurl_data,custom_link)
    shorturl = str(req)[42:-3]
    userId = userInfo['id']
    userName = userInfo['username']
    userFirstName = userInfo['first_name']
    userLastName = userInfo['last_name']
    cn = sqlite3.connect("zthdb.sqlite")
    cn.execute("PRAGMA ENCODING = 'utf8';")
    cn.text_factory = str
    cn.execute("CREATE TABLE IF NOT EXISTS user_comment(u_id MEDIUMINT,\
    u_name VARCHAR(100), u_first_name VARCHAR(100),\
    u_last_name VARCHAR(100), u_comment TEXT, u_time DATETIME);")
    cn.execute("INSERT INTO user_comment VALUES (?, ?, ?, ?, ?, ?);",\
    (userId, userName, userFirstName, userLastName,\
     userMessage, datetime.now()))
    cn.commit()
    cn.close()
    bot.sendMessage(chat_id=update.message.chat_id,
    text="http://a4l.ir/{} - Thanks. Our channel address: telegram.me/zerotoheroir"\
    .format(shorturl)
    )

def unknown(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Unknown Command!")


updater = Updater(token=myBotFatherToken)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s -\
 %(message)s', level=logging.INFO)

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

cm_handler = MessageHandler([Filters.text], getCm)
dispatcher.add_handler(cm_handler)

unknown_handler = MessageHandler([Filters.command], unknown)
dispatcher.add_handler(unknown_handler)
updater.start_polling()
updater.idle()
updater.stop()
