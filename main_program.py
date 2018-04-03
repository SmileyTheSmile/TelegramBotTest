from telegram.ext import Updater, MessageHandler, CommandHandler, Filters, ConversationHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from tools import *

def start(bot, update, user_data):
    update.message.reply_text("Приветствую! Я бот делающий всякие операции с картами (щедро подаренными мне людьми из Яндекса(ТМ)). В любой момент нашего разговора вы можете написать команду /stop чтобы всё остановить. Пожалуйста выберете язык./nGood day! I'm a bot that does stuff with maps, that were generously donated to me by people from Yandex(TM). At any point in our conversation you can use the command /stop to stop it. Please select your language.", reply_markup=markup)
    return 1

def stop(bot, update):
    if user_data['language'] == 'RU':
        update.message.reply_text('Хорошо. Чтобы начать разговор занаво напишите команду /start.', reply_markup=ReplyKeyboardRemove())
    elif user_data['language'] == 'EN':
        update.message.reply_text("Alright. To start a new conversation use the command /start.", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

def help(bot, update, user_data):
    if user_data['language'] == 'RU':
        update.message.reply_text('Я бот, делающий всякую бурду.')
    elif user_data['language'] == 'EN':
        update.message.reply_text("I'm a bot that does stuff or whatever.")
        
    
    
def beginning(bot, update, user_data):
    user_data['language'] = update.message.text
    if user_data['language'] == 'RU':
        update.message.reply_text('Что вы желаете сделать?\nа)Найти какое - нибудь место по адресу? (Напишите "Найти по адресу" если да)\nб)Найти что находится по определённым координатам? (Напишите "Найти по координатам" если да)')
        return 2
    elif user_data['language'] == 'EN':
        update.message.reply_text("What do you want me to do?\na)Find something according to it's address? (Reply with 'Find by address' if yes.)\nb)Find something according to it's coordinates? Reply with 'Find by coords' if yes.")
        return 2
    else:
        update.message.reply_text("I was unable to process whatever you wrote there.Please try again.\nЯ не понял что вы там написали. Пожалуйста попробуйте снова.")
        return 1

def first_choice(bot, update, user_data):
    if user_data['language'] == 'RU':
        if update.message.text == "Найти по адресу":
            update.message.reply_text('Напишите адрес объекта.')
            return 3
        elif update.message.text == "Найти по координатам":
            update.message.reply_text('Напишите координаты в таком формате: "43.34,34.43".')
            return 4
    elif user_data['language'] == 'EN':
        if update.message.text == "Find by address":
            update.message.reply_text("Please give me the object's address.")
            return 3
        elif update.message.text == "Find by coords":
            update.message.reply_text("Please give me the object's coordinates in this format: '43.34,34.43'.")
            return 4
    
def address_finder(bot, update, user_data):
    url = static_mapper(geocoder(update.message.text))
    if url != 'err1' or 'err2':
        if user_data['language'] == 'RU':
            text = ''
        elif user_data['language'] == 'EN':
            text = ''                
        bot.sendPhoto(
            update.message.chat.id,
            url,
            text
            )
        return ConversationHandler.END
    elif url == 'err1':
        if lan == 'RU':
            update.message.reply_text("По вашему запросу ничего не было найдено. Пожалуйста попробуйте снова.")
        elif lan == 'EN':
            update.message.reply_text("Nothing was found using the data you've given. Please try again")
        return 3
    elif url == 'err2':
        if lan == 'RU':
            update.message.reply_text("Во время выполнения вашего запроса возникла ошибка. Пожалуйста попробуйте снова.")
        elif lan == 'EN':
            update.message.reply_text("There was an error processing your request. Please try again.")
        return 3

def coords_finder(bot, update, user_data):
    url = static_mapper(update.message.text)
    request = requests.get(url)
    if request.status_code == 200:
        if user_data['language'] == 'RU':
            text = ''
        elif user_data['language'] == 'EN':
            text = ''                
        bot.sendPhoto(
            update.message.chat.id,
            address,
            text
            )
        return ConversationHandler.END
    else:
        if lan == 'RU':
            update.message.reply_text("Во время выполнения вашего запроса возникла ошибка. Пожалуйста попробуйте снова.")
        elif lan == 'EN':
            update.message.reply_text("There was an error processing your request. Please try again.")
        return 4


reply_keyboard = [['/start', '/stop'],
                  ['/help']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)


def main():
    updater = Updater('529760587:AAETCHDQCBvJoQQ76m66U0z5YOTT06i584o')
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("help", help))    
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            1: [MessageHandler(Filters.text, beginning)],
            2: [MessageHandler(Filters.text, first_choice)],
            3: [MessageHandler(Filters.text, address_finder)],
            4: [MessageHandler(Filters.text, coords_finder)],            
        },
        fallbacks=[CommandHandler('stop', stop)]
    )
    
    dp.add_handler(conv_handler) 
    dp.add_handler(CommandHandler("help", help))
    
    print('Bot has started...')
    
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()