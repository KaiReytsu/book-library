import json

import telebot
from book_repository.models import Book
from book_repository.serializers import BookSerializer
from django.conf import settings
from telebot.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           ReplyKeyboardMarkup)

#from django.core.management.base import BaseCommand

serail_book = []
bot = telebot.TeleBot(settings.TGTOKKEN)
keyboard = ReplyKeyboardMarkup(True, True)
keyboard.row('Список книг', 'Поиск по книгам')

@bot.message_handler(commands=['start'])
def start(msg):
    bot.send_message(msg.chat.id, 'Привет', reply_markup=keyboard)

@bot.message_handler(content_types=['text'])
def booklist(msg):
    global serial_book
    page = 1
    item_on_page = 2
    book = Book.objects.all()
    serial_book = []
    for item in book:
        serial_book.append(BookSerializer(item).data)
    count = len(serial_book) // item_on_page
    if len(serial_book) % item_on_page != 0:
        count +=1   
    if msg.text.lower() == 'список книг':
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(
            text=f'{page}/{count}', 
            callback_data=f' '),
               InlineKeyboardButton(
                text=f'Вперёд --->', 
                callback_data=
                "{\"method\":\"pagination\",\"NumberPage\":" + 
                str(page+1) + ",\"CountPage\":" + str(count)  + "}"))
        bot.send_message(
            msg.from_user.id, 
            f'{serial_book[(page-1)*item_on_page]["book_name"]},\n'
            f'{serial_book[((page-1)*item_on_page)+1]["book_name"]},', 
            reply_markup = markup)
    elif msg.text.lower() == 'поиск по книгам':
        # search_by = msg.text
        # book = Book.objects.filter(book_name = search_by)
        bot.send_message(msg.chat.id, 'В разработке')
    else:
        bot.send_message(msg.chat.id, 'Бот не обрабатывает, в разработке')

@bot.callback_query_handler(func=lambda call:True)
def callback_query(call):
    item_on_page = 2
    req = call.data.split('_')
    if 'pagination' in req[0]:
        json_string = json.loads(req[0])
        count = json_string['CountPage']
        page = json_string['NumberPage']
        markup = InlineKeyboardMarkup()
        if page == 1:
            markup.add(InlineKeyboardButton(
                            text=f'{page}/{count}', 
                            callback_data=f' '),
                       InlineKeyboardButton(
                            text=f'Вперёд --->',
                            callback_data="{\"method\":\"pagination\",\"NumberPage\":" + str(
                            page + 1) + ",\"CountPage\":" + str(count) + "}"))
        elif page == count:
            markup.add(InlineKeyboardButton(
                            text=f'<--- Назад',
                            callback_data="{\"method\":\"pagination\",\"NumberPage\":" + str(
                            page - 1) + ",\"CountPage\":" + str(count) + "}"),
                       InlineKeyboardButton(
                        text=f'{page}/{count}', 
                        callback_data=f' '))
        else:
            markup.add(InlineKeyboardButton(
                        text=f'<--- Назад', 
                        callback_data="{\"method\":\"pagination\",\"NumberPage\":" + str(
                            page-1) + ",\"CountPage\":" + str(count) + "}"),
                           InlineKeyboardButton(
                                text=f'{page}/{count}', 
                                callback_data=f' '),
                           InlineKeyboardButton(
                                text=f'Вперёд --->', 
                                callback_data="{\"method\":\"pagination\",\"NumberPage\":" + str(
                                    page+1) + ",\"CountPage\":" + str(count) + "}"))
        if len(serial_book) % item_on_page != 0 and count == (len(serial_book) // item_on_page) +1:
            bot.edit_message_text(f'{serial_book[(page-1)*item_on_page]["book_name"]},\n',
                                reply_markup = markup, 
                                chat_id=call.message.chat.id, 
                                message_id=call.message.message_id)
        
        bot.edit_message_text(f'{serial_book[(page-1)*item_on_page]["book_name"]},\n'
                                f'{serial_book[((page-1)*item_on_page)+1]["book_name"]},',
                                reply_markup = markup, 
                                chat_id=call.message.chat.id, 
                                message_id=call.message.message_id)



bot.infinity_polling()


# class Command(BaseCommand):

#     help = 'Implemented to Django application telegram bot setup command'

#     def handle(self, *args, **kwargs):
#         bot.enable_save_next_step_handlers(delay=2)
#         bot.load_next_step_handlers()								
#         bot.infinity_polling()											