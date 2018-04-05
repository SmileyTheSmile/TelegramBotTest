from telegram.ext import Updater, MessageHandler, CommandHandler, Filters, ConversationHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from tools import *

def start(bot, update):
    update.message.reply_text(" Приветствую! Я бот делающий всякие операции с картами (щедро подаренными мне людьми из Яндекса(ТМ)). В любой момент нашего разговора вы можете написать команду /stop чтобы всё остановить. Пожалуйста выберете язык.\n Good day! I'm a bot that does stuff with maps, that were generously donated to me by people from Yandex(TM). At any point in our conversation you can use the command /stop to stop it. Please select your language.", reply_markup=markup1)
    return 1

def stop(bot, update, user_data):
    update.message.reply_text('Хорошо. Чтобы начать разговор занаво напишите команду /start.\nAlright. To start a new conversation use the command /start.', reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

def help(bot, update):
    update.message.reply_text("Я бот, делающий всякую бурду.\nI'm a bot that does stuff or whatever.")
    
    
def beginning(bot, update, user_data, chat_data):
    user_data['language'] = update.message.text
    if user_data['language'] == 'RU':
        update.message.reply_text('Что вы желаете сделать?\n а)Найти какое - нибудь место по адресу? (Напишите "А" если да)\n б)Найти что находится по определённым координатам? (Напишите "Б" если да)', reply_markup=markup2ru)
        return 2
    elif user_data['language'] == 'EN':
        update.message.reply_text("What do you want me to do?\n a)Find something according to it's address? (Reply with 'A' if yes.)\n b)Find something according to it's coordinates? Reply with 'B' if yes.", reply_markup=markup2en)
        return 2
    else:
        update.message.reply_text("I was unable to process whatever you wrote there.Please try again.\n Я не понял что вы там написали. Пожалуйста попробуйте снова.", reply_markup=stop_markup)
        return 1

def first_choice(bot, update, user_data, chat_data):
    if user_data['language'] == 'RU':
        if update.message.text == "А" or update.message.text =='а':
            update.message.reply_text('Напишите адрес объекта.', reply_markup=stop_markup)
            return 3
        elif update.message.text == "Б" or update.message.text =='б':
            update.message.reply_text('Напишите координаты в таком формате: "43.34,34.43".', reply_markup=stop_markup)
            return 4
        else:
            update.message.reply_text("Такого ответа не было! Попробуйте снова.", reply_markup=stop_markup)
            return 2          
    elif user_data['language'] == 'EN':
        if update.message.text == "A" or update.message.text =='a':
            update.message.reply_text("Please give me the object's address.", reply_markup=stop_markup)
            return 3
        elif update.message.text == "B" or update.message.text =='b':
            update.message.reply_text("Please give me the object's coordinates in this format: '43.34,34.43'.", reply_markup=stop_markup)
            return 4
        else:
            update.message.reply_text("There was no option like that! Try again.", reply_markup=stop_markup)
            return 2 
    
    
def address_finder(bot, update, user_data, chat_data):
    url = static_mapper(geocoder(update.message.text))
    if url != 'err1' or url !='err2':
        if user_data['language'] == 'RU':
            text = ' Что вы хотите сделать теперь?\n а) Найти ещё одну точку\n б)Найти предприятия вокруг этой точки?\n в) Завершить обслуживание'
            markup = markup3ru
        elif user_data['language'] == 'EN':
            text = ' What do you want to do now?\n a) Find another point\n b)Find the organisations around the point?\n c) Finish the conversation'    
            markup = markup3en
        bot.sendPhoto(
            update.message.chat.id,
            url[0],
            text,
            reply_markup=markup
            )
        user_data['last_search'] = url[1]
        return 5
    elif url == 'err1':
        if lan == 'RU':
            update.message.reply_text("По вашему запросу ничего не было найдено. Пожалуйста попробуйте снова.", reply_markup=stop_markup)
        elif lan == 'EN':
            update.message.reply_text("Nothing was found using the data you've given. Please try again", reply_markup=stop_markup)
        return 3
    elif url == 'err2':
        if lan == 'RU':
            update.message.reply_text("Во время выполнения вашего запроса возникла ошибка. Пожалуйста попробуйте снова.", reply_markup=stop_markup)
        elif lan == 'EN':
            update.message.reply_text("There was an error processing your request. Please try again.", reply_markup=stop_markup)
        return 3

def coords_finder(bot, update, user_data, chat_data):
    url = static_mapper((update.message.text, ('0.02', '0.02')))
    request = requests.get(url[0])
    if request.status_code == 200:
        if user_data['language'] == 'RU':
            text = ' Что вы хотите сделать теперь?\n а) Найти ещё одну точку\n б)Найти предприятия вокруг этой точки?\n в) Завершить обслуживание'
            markup = markup3ru
        elif user_data['language'] == 'EN':
            text = ' What do you want to do now?\n a) Find another point\n b)Find the organisations around the point?\n c) Finish the conversation'      
            markup = markup3en
        bot.sendPhoto(
            update.message.chat.id,
            url[0],
            text,
            reply_markup=markup
            )
        user_data['last_search'] = url[1]
        return 5
    else:
        if user_data['language'] == 'RU':
            update.message.reply_text("Во время выполнения вашего запроса возникла ошибка. Пожалуйста попробуйте снова.", reply_markup=stop_markup)
        elif user_data['language'] == 'EN':
            update.message.reply_text("There was an error processing your request. Please try again.", reply_markup=stop_markup)
        return 4
    
def second_choice(bot, update, user_data, chat_data):
    if user_data['language'] == 'RU':
        if update.message.text == "А" or update.message.text == 'а':
            update.message.reply_text('Что вы желаете сделать?\n а) Найти какое - нибудь место по адресу? (Напишите "А" если да)\n б)Найти что находится по определённым координатам? (Напишите "Б" если да)', reply_markup=choice_keyboard2ru)
            return 2
        elif update.message.text == "Б" or update.message.text == 'б':
            update.message.reply_text('В каком радиусе от найденной точки нужно найти организации?', reply_markup=stop_markup)
            return 6
        elif update.message.text == "В" or update.message.text == 'в':
            update.message.reply_text('Хорошо. Чтобы начать разговор занаво напишите команду /start.', reply_markup=ReplyKeyboardRemove())
            return ConversationHandler.END
        else:
            update.message.reply_text("Такого ответа не было! Попробуйте снова.")
            return 5         
    elif user_data['language'] == 'EN':
        if update.message.text == "A" or update.message.text == 'a':
            update.message.reply_text('What do you want to do?\n a)Find a place according to its address? (Reply with "A" if yes)\n b)Find something according to its coordinates? (Reply with "B" if yes)', reply_markup=choice_keyboard2en)
            return 2
        elif update.message.text == "B" or update.message.text == 'b':
            update.message.reply_text('At what radius from the point would you like to find the organisations?', reply_markup=stop_markup)
            return 6
        elif update.message.text == "C" or update.message.text == 'c':
            update.message.reply_text("Alright. To start a new conversation use the command /start.", reply_markup=ReplyKeyboardRemove())
            return ConversationHandler.END
        else:
            update.message.reply_text("That ain't an answer! Try again.")
            return 5      

def organisations_finder(bot, update, user_data, chat_data):
    spn = update.message.text
    organisations = get_organisation(user_data['last_search'], spn)
    if organisations != 'err5':
        url = static_mapper((user_data['last_search'], ('0.02', '0.02')), organisations)
        request = requests.get(url[0])
        if request.status_code == 200:
            if user_data['language'] == 'RU':
                text = ' Что вы хотите сделать теперь?\n а) Найти ещё одну точку\n б) Завершить обслуживание'
                markup = markup2ru
            elif user_data['language'] == 'EN':
                text = ' What do you want to do now?\n a) Find another point\n b) Finish the conversation'   
                markup = markup2en
            bot.sendPhoto(
                update.message.chat.id,
                url[0],
                text,
                reply_markup = markup
                )
            user_data['last_search'] = url[1]
            return 7
        else:
            if user_data['language'] == 'RU':
                update.message.reply_text("Во время выполнения вашего запроса возникла ошибка. Пожалуйста попробуйте снова.")
            elif user_data['language'] == 'EN':
                update.message.reply_text("There was an error processing your request. Please try again.")
    else:
        if user_data['language'] == 'RU':
            update.message.reply_text("Ничего не было найдено. Попробуйте поискать поближе к цивилизации.")
        elif user_data['language'] == 'EN':
            update.message.reply_text("Nothing was found. Try searching somewhere closer to civilization.")
    return 6
    
def third_choice(bot, update, user_data, chat_data):
    if user_data['language'] == 'RU':
        if update.message.text == "А" or update.message.text == 'а':
            update.message.reply_text('Что вы желаете сделать?\n а) Найти какое - нибудь место по адресу? (Напишите "А" если да)\n б)Найти что находится по определённым координатам? (Напишите "Б" если да)', reply_markup=choice_keyboard2ru)
            return 2
        elif update.message.text == "Б" or update.message.text == 'б':
            update.message.reply_text('Хорошо. Чтобы начать разговор занаво напишите команду /start.', reply_markup=ReplyKeyboardRemove())
            return ConversationHandler.END
        else:
            update.message.reply_text("Такого ответа не было! Попробуйте снова.")
            return 5         
    elif user_data['language'] == 'EN':
        if update.message.text == "A" or update.message.text == 'a':
            update.message.reply_text('What do you want to do?\n a)Find a place according to its address? (Reply with "A" if yes)\n b)Find something according to its coordinates? (Reply with "B" if yes)', reply_markup=choice_keyboard2en)
            return 2
        elif update.message.text == "B" or update.message.text == 'b':
            update.message.reply_text("Alright. To start a new conversation use the command /start.", reply_markup=ReplyKeyboardRemove())
            return ConversationHandler.END
        else:
            update.message.reply_text("That ain't an answer! Try again.")
            return 5      

stop_keyboard = [['/start', '/stop']]
choice_keyboard1 = [['RU', 'EN'], ['/stop']]
choice_keyboard2ru = [['А', 'Б'], ['/stop']]
choice_keyboard2en = [['A', 'B'], ['/stop']]
choice_keyboard3ru = [['А', 'Б', 'В'], ['/stop']]
choice_keyboard3en = [['A', 'B', 'C'], ['/stop']]
stop_markup = ReplyKeyboardMarkup(stop_keyboard, one_time_keyboard=False)
markup1 = ReplyKeyboardMarkup(choice_keyboard1, one_time_keyboard=False)
markup2ru = ReplyKeyboardMarkup(choice_keyboard2ru, one_time_keyboard=False)
markup2en = ReplyKeyboardMarkup(choice_keyboard2en, one_time_keyboard=False)
markup3ru = ReplyKeyboardMarkup(choice_keyboard3ru, one_time_keyboard=False)
markup3en = ReplyKeyboardMarkup(choice_keyboard3en, one_time_keyboard=False)


def main():
    updater = Updater('529760587:AAETCHDQCBvJoQQ76m66U0z5YOTT06i584o')
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("help", help))    
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            1: [MessageHandler(Filters.text, beginning, pass_chat_data=True, pass_user_data=True)],
            2: [MessageHandler(Filters.text, first_choice, pass_chat_data=True, pass_user_data=True)],
            3: [MessageHandler(Filters.text, address_finder, pass_chat_data=True, pass_user_data=True)],
            4: [MessageHandler(Filters.text, coords_finder, pass_chat_data=True, pass_user_data=True)],  
            5: [MessageHandler(Filters.text, second_choice, pass_chat_data=True, pass_user_data=True)],
            6: [MessageHandler(Filters.text, organisations_finder, pass_chat_data=True, pass_user_data=True)],
            7: [MessageHandler(Filters.text, third_choice, pass_chat_data=True, pass_user_data=True)]
        },
        fallbacks=[CommandHandler('stop', stop, pass_user_data=True)]
    )
    
    dp.add_handler(conv_handler) 
    dp.add_handler(CommandHandler("help", help))
    
    print('Bot has started...')
    
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()