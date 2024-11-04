# This bot is needed to connect two people and their subsequent anonymous communication
# Avaiable commands:
# `/start` - Just send you a messsage how to start
# `/find` - Find a person you can contact
# `/stop` - Stop active conversation

import telebot 
from telebot import types


bot = telebot.TeleBot('7893890642:AAHXQOO1LvifXZJnbQJG8iwvL5kCzkFfK7Q')


users = {}


freeid = None


@bot.message_handler(commands=['start'])
def start(message: types.Message):
    bot.send_message(message.chat.id, 'Пиши /help для проссмотра всех команд')


@bot.message_handler(commands=['help'])
def start(message: types.Message):
    bot.send_message(message.chat.id, 'Искать собеседника /find; остановть поиск или прекратить общение /stop; Посмотреть мемы /mem')
    
@bot.message_handler(commands=['mem'])
def send_mem(message):
    with open('images/mem1.jpg', 'rb') as f:
        bot.send_photo(message.chat.id, f)

@bot.message_handler(commands=['find'])
def find(message: types.Message):      
    global freeid

    if message.chat.id not in users:
        bot.send_message(message.chat.id, 'Поиск...')

        if freeid is None:
            freeid = message.chat.id
        else:
            # Question:
            # Is there any way to simplify this like `bot.send_message([message.chat.id, freeid], 'Founded!')`?
            bot.send_message(message.chat.id, 'Собеседник найден!!')
            bot.send_message(freeid, 'Собеседник найден!')

            users[freeid] = message.chat.id
            users[message.chat.id] = freeid
            freeid = None
            
        print(users, freeid) # Debug purpose, you can remove that line
    else:
        bot.send_message(message.chat.id, 'Заткнись!')

# `/stop` command handler
#
# That command stops your current conversation (if it exist)
#
# That command according to the following principle:
# 1. You have written `/stop` command
# 2. If you are not have active dialog or you are not in search, bot sends you 'You are not in search!'
# 3. If you are in active dialog:
#   3.1. Bot sends you 'Stopping...'
#   3.2. Bot sends 'Your opponent is leavin`...' to your opponent
#   3.3. {your_opponent_chat_id, your_chat_id} removes from `users`
#   3.4. {your_chat_id, your_opponent_chat_id} removes from `users`
# 4. If you are only in search:
#   4.1. Bot sends you 'Stopping...'
#   4.2. `freeid` updated with `None`
@bot.message_handler(commands=['stop'])
def stop(message: types.Message):
    global freeid

    if message.chat.id in users:
        bot.send_message(message.chat.id, 'Ты прекратил общение...')
        bot.send_message(users[message.chat.id], 'Твой собеседник прекратил общение`...')

        del users[users[message.chat.id]]
        del users[message.chat.id]
        
        print(users, freeid) # Debug purpose, you can remove that line
    elif message.chat.id == freeid:
        bot.send_message(message.chat.id, 'Остановка...')
        freeid = None

        print(users, freeid) # Debug purpose, you can remove that line
    else:
        bot.send_message(message.chat.id, 'Вы не находитесь в поиске!')

# message handler for conversation
#
# That handler needed to send message from one opponent to another
# If you are not in `users`, you will recieve a message 'No one can hear you...'
# Otherwise all your messages are sent to your opponent
#
# Questions:
# 1. Is there any way to improve readability like `content_types=['all']`?
# 2. Is there any way to register this message handler only when i found the opponent?
@bot.message_handler(content_types=['animation', 'audio', 'contact', 'dice', 'document', 'location', 'photo', 'poll', 'sticker', 'text', 'venue', 'video', 'video_note', 'voice'])
def chatting(message: types.Message):
    if message.chat.id in users:
        bot.copy_message(users[message.chat.id], users[users[message.chat.id]], message.id)
    else:
        bot.send_message(message.chat.id, 'Никто тебя не слышит...')

bot.infinity_polling(skip_pending=True)

        
