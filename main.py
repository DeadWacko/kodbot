from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from config import token
import keyboard
import random

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random

bot = Bot(token=token)
dp = Dispatcher(bot)


#флаги
Flag_mail = False
flag_mail_pin = False

mail_pin = 0

def send_mail(input_mail,send_pin):
    fromaddr = 'kodbot.mail@gmail.com'
    toaddrs = input_mail
    # Writing the message (this message will appear in the email)
    msg = "pin" + send_pin
    # Gmail Login
    username = 'kodbot.mail@gmail.com'
    password = 'kodbot123'
    # Sending the mail
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username, password)
    server.sendmail(fromaddr, toaddrs, msg)
    server.quit()


#bot.py
@dp.message_handler(commands=['start'])
async def process_command_1(message: types.Message):
    await message.reply("Привет, выбери свой статус :3", reply_markup=keyboard.start_keyboard_markup)


@dp.callback_query_handler(text='event_jedi_button')
async def event_jedi_button(callback: types.CallbackQuery):
    global Flag_mail
    await callback.message.answer('Шикарно, давай тебя зарегестрируем. Введи свою корпоративную почту.\n'
                                  'П.С. Меня не обманешь:3')
    await callback.message.answer('жду почту!')
    Flag_mail = True

@dp.message_handler()
async def input_mail(msg: types.Message):
    global Flag_mail
    global mail_pin
    global flag_mail_pin
    new_messadge = ""
    old_messadge = ""
    if Flag_mail:
        new_messadge = msg.text
        if "@kodland.team" in new_messadge:
            await bot.send_message(msg.from_user.id, "Почта подходит,\n, секундочку...отправляю код")
            Flag_mail = False
            mail_pin = random.randint(100000,999999)

            send_mail("kodbot.mail@gmail.com", str(mail_pin))
            #await bot.send_message(msg.from_user.id, mail_pin)
            await bot.send_message(msg.from_user.id, "отправил код")
            flag_mail_pin = True
            old_messadge = new_messadge

        else:
            await bot.send_message(msg.from_user.id, "ТЫ ШПИОН")

    if flag_mail_pin:
        print("Это код")
        new_messedge = msg.text
        print(new_messedge)
        print(old_messadge)
        flag_new_message = False
        if new_messedge != old_messadge:
            flag_new_message = True

            if new_messedge == str(mail_pin) and flag_new_message:
                print("Код подошел")
                await bot.send_message(msg.from_user.id, "Код подошел:333 я тебя проверил")
                await bot.send_message(msg.from_user.id, "Теперь тебе доступно меню преподавателя. Поздравляю тебя :3",
                                       reply_markup=keyboard.jedi_menu_keyboard_markup)




                mail_pin = 0
                flag_mail_pin = False
                flag_new_message = False
            else:
                await bot.send_message(msg.from_user.id, "Код не подошел, давай еще раз")






if __name__ == '__main__':
    executor.start_polling(dp)

