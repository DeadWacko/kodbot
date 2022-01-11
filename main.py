from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from config import token
import keyboard


import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random
import json
bot = Bot(token=token)
dp = Dispatcher(bot)


#флаги
Flag_mail = False
flag_mail_pin = False
flag_new_group = False

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


#функция печати нынешних групп
def print_group_json():
    with open('data.JSON', 'r',encoding="utf-8") as f:
        json_data = json.load(f)
        str = ""
        for i in json_data["jedi"]["Костюкевич Михаил Константинович"]["podavans_group"].keys():
            str += i
        f.close()
        return str
#функция добавляющая группу и шаблон для учеников
def add_new_group_json(input_new_group,lesson_day,lesson_time):

    str = print_group_json()
    print(print_group_json())
    print(input_new_group)
    if input_new_group not in str:
        with open('data.JSON', 'r', encoding="utf-8") as f:
            json_data = json.load(f)

            x = {"last_lesson": "0",
          "lesson_day": f"{lesson_day}",
          "lesson_time": f"{lesson_time}",
          "podavans": {}}




            json_data["jedi"]["Костюкевич Михаил Константинович"]["podavans_group"][input_new_group] = x

        with open('data.JSON', 'w', encoding="utf-8") as f:
            f.write(json.dumps(json_data, ensure_ascii=False))
            f.close()
    else:
        print("Группа есть")





#стартовая клавиатура
@dp.message_handler(commands=['start'])
async def process_command_1(message: types.Message):
    await message.reply("Привет, выбери свой статус :3", reply_markup=keyboard.start_keyboard_markup)

#регистрация преподавателя
@dp.callback_query_handler(text='event_jedi_button')
async def event_jedi_button(callback: types.CallbackQuery):
    global Flag_mail
    await callback.message.answer('Шикарно, давай тебя зарегестрируем. Введи свою корпоративную почту.\n'
                                  'П.С. Меня не обманешь:3')
    await callback.message.answer('жду почту!')
    Flag_mail = True

#ответы на текстовые сообщения
@dp.message_handler()
async def input_mail(msg: types.Message):
    global Flag_mail
    global mail_pin
    global flag_mail_pin
    global flag_new_group
    new_messadge = ""
    old_messadge = ""
    #добавление почты
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
    #проверка pin-кода с почты
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
                old_messadge = new_messadge
            else:
                await bot.send_message(msg.from_user.id, "Код не подошел, давай еще раз")
    #добавление новой группы
    if flag_new_group:

        new_messedge = msg.text

        flag_new_message = False
        if new_messedge != old_messadge:
            flag_new_message = True

            if  flag_new_message:
                print("Код подошел")

                print(new_messedge.split("\n")[0])
                await bot.send_message(msg.from_user.id, "Секундочку...")


                flag_new_group = False
                flag_new_message = False
                old_messadge = new_messadge
                name_group = new_messedge.split("\n")[0]
                day_group = new_messedge.split("\n")[1]
                time_group = new_messedge.split("\n")[2]

                add_new_group_json(input_new_group=name_group, lesson_day=day_group,
                                   lesson_time=time_group)



                await bot.send_message(msg.from_user.id, f"ок\nдобавлена новая группа:\n название группы: {name_group} \n день занятий: {day_group}\n Время занятий: {time_group}")




            else:
                await bot.send_message(msg.from_user.id, "Какая-то ерунда")

#добавление группы
@dp.callback_query_handler(text='event_add_group_button')
async def event_jedi_button(callback: types.CallbackQuery):
    global flag_new_group
    await callback.message.answer("Давай добавим новую группу по такому шаблону(одним сообщением):\n\nНазвание группы \nдень недели (по счету) \nвремя занятия \n\nПример:\n\nNewmini2934_ПТ-18 \n5 \n18:00"
)
    flag_new_group = True

#Просмотр статистики
@dp.callback_query_handler(text='event_show_stats_button')
async def event_jedi_button(callback: types.CallbackQuery):
    await callback.message.answer("Скоро здесь будет раздел со статистикой")
    await callback.message.answer("Верну тебя обратно:",reply_markup=keyboard.jedi_menu_keyboard_markup)





if __name__ == '__main__':
    executor.start_polling(dp)

