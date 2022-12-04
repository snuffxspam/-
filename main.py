from sqlworker import *
from tk import Token
from telebot import types
import telebot as t
import time
from threading import Timer
from datetime import datetime
 

bot = t.TeleBot(Token, threaded=False)


def hello(message_id, message, mname):
    bot.send_message(message_id, message)
    Delete_event(mname, message)
 
class RepeatedTimer(object):
    nruns = 0
    
    def __init__(self, times, function, *args, **kwargs):
        self._timer     = None
        self.function   = function
        self.times      = times
        self.args       = args
        self.kwargs     = kwargs
        self.is_running  = False
        self.start()
 
    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, tm=type(self), **self.kwargs)
        
        
    def start(self):
        
        if self.times[1] !=-1 and type(self).nruns >= self.times[1]:
            self.stop() 
            return 
        
        if not self.is_running:
            self._timer = Timer(self.times[0], self._run)
            self._timer.start()
            self.is_running = True
            
            
    def stop(self):
        self._timer.cancel()
        self.is_running = False
 
 
def timer(start, message_id, message, mname,**kwargs):
    now = datetime.today().strftime("%H:%M:%S")
    tm = kwargs.get('tm')
    

    if str(now) == start:
        hello(message_id, message, mname) 
        tm.nruns += 1 
        
 
def main():
    time.sleep(100)
    print('end main')

bot = t.TeleBot(Token, threaded=False)

event_dict = {}

class Events:
    def __init__(self, name):
        self.name = name
        self.desrciption = None
        self.event_time = None
        self.reminder_time = None

@bot.message_handler(commands=['start'])
def Welcome(message):
    try:
        if not Checker(message.from_user.first_name.split()):
           Create_User(message.from_user.first_name)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        b1 = types.KeyboardButton("посмотреть напоминания")
        b2 = types.KeyboardButton("создать напоминание") 
        markup.add(b1)
        markup.add(b2)
        msg = bot.send_message(message.chat.id, f"Добро пожаловать, {message.from_user.first_name}", reply_markup=markup)
    except Exception as err:
        print(err)

@bot.message_handler(content_types=['text'])
def main_menu(message):
    try:
        if message.text == 'посмотреть напоминания' :
            keyboard = types.InlineKeyboardMarkup()
            for x in Print_Users(message.from_user.first_name):
                b1 = types.InlineKeyboardButton(x[1], callback_data = x[1])
                keyboard.add(b1)
            msg = bot.send_message(message.chat.id, "События", reply_markup=keyboard)
        elif message.text == 'создать напоминание' :
            markupdel = types.ReplyKeyboardRemove()
            msg = bot.send_message(message.chat.id, "Введите название события:", reply_markup=markupdel)
            bot.register_next_step_handler(msg, Reminder_name)
    except Exception as err:
        print(err)

def Reminder_name(message):
    try:
        name = message.text
        event = Events(name)
        event_dict[message.chat.id] = event
        msg = bot.send_message(message.chat.id, "Введите описание события: (если хотите пропустить, напишите '-')")
        bot.register_next_step_handler(msg, Reminder_description)
    except Exception as err:
        print(err)

def Reminder_description(message):
    try:
        description = message.text
        if len(description) > 128:
            msg = bot.send_message(message.chat.id, "Введите описание события: (не больше 128 символов)")
            bot.register_next_step_handler(msg, Reminder_description)
            return
        event = event_dict[message.chat.id]
        event.description = description
        msg = bot.send_message(message.chat.id, "Введите время события: (xx:xx)")
        bot.register_next_step_handler(msg, Reminder_event_time)
    except Exception as err:
        print(err)

def Reminder_event_time(message):   
    try:
        event_time = message.text
        if event_time[2] != ":" or not(event_time[0:2].isdigit()) or not(event_time[3:5].isdigit()):
            msg = bot.send_message(message.chat.id, "Введите время события в правильном формате: (xx:xx)")
            bot.register_next_step_handler(msg, Reminder_event_time)
            return
        event = event_dict[message.chat.id]
        event.event_time = event_time
        msg = bot.send_message(message.chat.id, "Введите время напоминания: (xx:xx)")
        bot.register_next_step_handler(msg, Reminder_time)
    except Exception as err:
        print(err)

def Reminder_time(message):
    try:
        reminder_time = message.text
        if reminder_time[2] != ":" or not(reminder_time[0:2].isdigit()) or not(reminder_time[3:5].isdigit()):
            msg = bot.send_message(message.chat.id, "Введите время напоминания в правильном формате: (xx:xx)")
            bot.register_next_step_handler(msg, Reminder_time)
            return
        event = event_dict[message.chat.id]
        event.reminder_time = reminder_time
        reminder_time += ":00"
        New_event(message.from_user.first_name, event.name, event.description, event.event_time, event.reminder_time)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        b1 = types.KeyboardButton("посмотреть напоминания")
        b2 = types.KeyboardButton("создать напоминание")
        markup.add(b1)
        markup.add(b2)
        s = RepeatedTimer((1.,1), timer, reminder_time, message.chat.id, event.name, message.from_user.first_name)
        msg = bot.send_message(message.chat.id, "Событие создано", reply_markup=markup)
    except Exception as err:
        print(err)

@bot.callback_query_handler(func=lambda call: True)
def xall(call):
    try:
        for x in Print_Users(bot.get_chat_member(call.message.chat.id, call.message.chat.id).user.first_name):
            if x[1] == call.data:
                user = call.data
                keyboard = types.InlineKeyboardMarkup()
                b1 = types.InlineKeyboardButton("Удалить событие", callback_data = x[1]+"delete")
                b2 = types.InlineKeyboardButton("Назад", callback_data = "back")
                keyboard.add(b1)
                keyboard.add(b2)
                bot.send_message(call.message.chat.id, f"{x[1]}\nОписание - {x[2]}\nВремя события - {x[3]}\nВремя напоминания события - {x[4]}", reply_markup=keyboard)
        if "delete" in call.data:
            Delete_event(bot.get_chat_member(call.message.chat.id, call.message.chat.id).user.first_name, call.data[:-6:])
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            b1 = types.KeyboardButton("посмотреть напоминания")
            b2 = types.KeyboardButton("создать напоминание")
            markup.add(b1)
            markup.add(b2)
            msg = bot.send_message(call.message.chat.id, f"Добро пожаловать, {bot.get_chat_member(call.message.chat.id, call.message.chat.id).user.first_name}", reply_markup=markup)
        elif "back" == call.data:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            b1 = types.KeyboardButton("посмотреть напоминания")
            b2 = types.KeyboardButton("создать напоминание")
            markup.add(b1)
            markup.add(b2)
            msg = bot.send_message(call.message.chat.id, f"Добро пожаловать, {bot.get_chat_member(call.message.chat.id, call.message.chat.id).user.first_name}", reply_markup=markup)
    except Exception as err:
        print(err)

bot.polling(none_stop=True)