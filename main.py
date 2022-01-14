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

import working_with_json


import datetime

bot = Bot(token=token)
dp = Dispatcher(bot)

# флаги
Flag_mail = False
flag_mail_pin = False
flag_new_group = False


def send_mail(input_mail, send_pin):
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


# функция печати нынешних групп    ###ПЕРЕДЕЛАТЬ
def print_group_json():
    with open('data.JSON', 'r', encoding="utf-8") as f:
        json_data = json.load(f)
        str = ""
        for i in json_data["jedi"]["Костюкевич Михаил Константинович"]["podavans_group"].keys():
            str += i
        f.close()
        return str


# функция добавляющая группу и шаблон для учеников
def add_new_group_json(input_new_group, lesson_day, lesson_time):
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


# функция добавления ученика в группу
def add_new_podavan_json(input_group, nik_telegram, podavan_name):
    str = print_group_json()
    print(print_group_json())
    print(input_group)
    if input_group in str:
        with open('data.JSON', 'r', encoding="utf-8") as f:
            json_data = json.load(f)

            x = {
                "podavan_name": f"{podavan_name}",
                "посещаемость": "0",
                "оценка уроков": {
                    "1": "0",
                    "2": "0",
                    "3": "0",
                    "4": "0",
                    "5": "0",
                    "6": "0",
                    "7": "0"
                },
                "рейтинг в боте": "0"
            }

            json_data["jedi"]["Костюкевич Михаил Константинович"]["podavans_group"][input_group]["podavans"][
                nik_telegram] = x

        with open('data.JSON', 'w', encoding="utf-8") as f:
            f.write(json.dumps(json_data, ensure_ascii=False))
            f.close()
    else:
        print("Такой группы нет")


# стартовая клавиатура
@dp.message_handler(commands=['start'])
async def process_command_1(message: types.Message):
    await message.reply("Привет, выбери свой статус :3", reply_markup=keyboard.start_keyboard_markup)


# регистрация преподавателя
@dp.callback_query_handler(text='event_jedi_button')
async def event_jedi_button(callback: types.CallbackQuery):
    await callback.message.answer('Так, давай-ка я проверю, не заходил ли ты раньше,секундочку...')
    if not working_with_json.json_check(required_verification="jedi",
                                        jedi_telegram_username=callback["from"]["username"]):
        await callback.message.answer('Ага, ты здесь впервые, давайка тебя добавим:3')
        await callback.message.answer('Секундочку, создаю для тебя директорию...')
        #
        #
        # Создаем пользователя(добавить шаблон для него, но без почты. для добавления почты необходима отдельная ф-я.
        #
        #
        working_with_json.json_add_new_jedi(jedi_telegram_username=callback["from"]["username"])
        # print(callback)
        await callback.message.answer(
            'Готово.\n Но теперь давай проверим тебя. Введи свою корпоративную почту, я вышлю тебе код.\n'
            'П.с. у тебя будет всего 5 попыток, после этого я удалю тебя :с')

        #
        #
        # Меняем состояние пользователя на "Ждем почту"
        # Ожидаем почту в ф-и input_text_msg
        #
        #
        working_with_json.json_change_flag_state(new_flag_state="Flag_mail",
                                                 telegram_username=callback["from"]["username"])
    else:
        await callback.message.answer('Ты уже есть, кыш атседа')
        await callback.message.answer('Вот тебе стартовая клавиатура преподавателя',
                                      reply_markup=keyboard.jedi_menu_keyboard_markup)


# TODO ответы на текстовые сообщения (input_text_msg)
#     ВЕТКА ПРЕПОДАВАТЕЛЯ_______________________________________________________________________________________________
#     1) Обработка Flag_mail(получение почты -> отправка на почту pin_кода -> смена флага на mail_pin ->
#         -> добавление pin_кода в data2.json)    ✅
#     2) Обработка mail_pin(Получение пин-кода -> сравнение pin-кода из сообщения с пин-кодом из data2.json    ✅
#     3) Обработка Flag_new_group (создание новой группы -> генерация пин-кода для этой группы + добавление этого пин-кода) ✅
#     ВЕТКА УЧЕНИКА_____________________________________________________________________________________________________
#     1) Функция обработки нажатия кнопки УЧЕНИК ✅
#     2) Обработка пин-кода ученика , чтобы его добавить в правильную группу  ✅
#     3)Функция для напоминаний о предстоящем уроке
#     5)функция рассылки напоминания


# ответы на текстовые сообщения
@dp.message_handler()
async def input_text_msg(msg: types.Message):
    old_messadge = ""
    new_messedge = ""
    input_flag_state = working_with_json.json_read_flag_state(telegram_username=msg.from_user.username)
    print(input_flag_state)

    # ✅
    if input_flag_state == "Flag_mail":
        new_messadge = msg.text
        if "@kodland.team" in new_messadge:
            await bot.send_message(msg.from_user.id, "Почта подходит,\n, секундочку...отправляю код")
            # создаем пин код`      ✅
            mail_pin = random.randint(100000, 999999)
            # отправляем код на почту      ✅
            send_mail("kodbot.mail@gmail.com", str(mail_pin))

            # добавляем код в date2.json    ✅
            working_with_json.json_change_mail_pin(new_mail_pin=mail_pin, telegram_username=msg.from_user.username)

            await bot.send_message(msg.from_user.id, "отправил код")

            old_messadge = new_messadge
            # меняем состояние флага преподавателя на flag_mail_pin     ✅
            working_with_json.json_change_flag_state(new_flag_state="flag_mail_pin",
                                                     telegram_username=msg["from"]["username"])
            #
            #
            # Тут нужно добавить эту почту в json
            #
            #
            #
            #

            print(working_with_json.json_read_flag_state(telegram_username=msg.from_user.username))

        else:
            await bot.send_message(msg.from_user.id, "ТЫ ШПИОН")
    # ✅
    elif input_flag_state == "flag_mail_pin":
        ##############################################################
        # проверка pin-кода с почты                                  #
        ##############################################################

        new_messedge = msg.text  # ИЗБАВИТЬСЯ ОТ ЭТОГО БЕЗОБРАЗИЯ

        # меняем состояние флага преподавателя на " "          ✅
        working_with_json.json_change_flag_state(new_flag_state="  ",
                                                 telegram_username=msg["from"]["username"])
        # читаем код с почты для авторизации почты ✅
        mail_pin = working_with_json.json_read_mail_pin(telegram_username=msg["from"]["username"])
        if new_messedge == str(mail_pin):
            await bot.send_message(msg.from_user.id, "Готово,код подошел,я тебя проверил:3",
                                   reply_markup=keyboard.jedi_menu_keyboard_markup)

        # если подошел код - загружаем стартовую клавиатуру преподавателя ✅
        #
        old_messadge = new_messedge
    # ✅
    elif input_flag_state == "Flag_new_group":
        new_messedge = msg.text

        # print(new_messedge)
        name_group = new_messedge.split("\n")[0]
        day_group = new_messedge.split("\n")[1]
        time_group = new_messedge.split("\n")[2]
        last_lesson_group = new_messedge.split("\n")[3]
        course_name_group = new_messedge.split("\n")[4]

        group_auth_pin = str(random.randint(9999, 999999))
        #
        #
        #
        #
        # добавить проверку на пин. нет ли такого среди других групп
        #
        #
        #
        #

        working_with_json.json_add_new_group(group_name=name_group, lesson_day=day_group, lesson_time=time_group,
                                             number_last_lesson=last_lesson_group, course_name=course_name_group,
                                             jedi_telegram_username=msg["from"]["username"],
                                             auth_padawan_pin=group_auth_pin)

        await bot.send_message(msg.from_user.id, "Группа добавлена. Чтобы твои ученики смогли попасть в свою группу -"
                                                 f" передай им этот код авторизации\n\n\n {group_auth_pin}",
                               reply_markup=keyboard.jedi_menu_keyboard_markup)

        working_with_json.json_change_flag_state(new_flag_state="  ",
                                                 telegram_username=msg["from"]["username"])

    # ✅
    elif input_flag_state == "flag_add_padawan":
        new_messedge = msg.text
        padawan_pin = new_messedge.split("\n")[0]
        padawan_full_name = new_messedge.split("\n")[1]
        a = "test"
        b = "test"
        c = "test"
        d = "test"
        if working_with_json.json_add_new_padawan(padawan_telegram_username=msg.from_user.username,
                                                  auth_padawan_pin=padawan_pin,
                                                  padawan_full_name=padawan_full_name):
            await bot.send_message(msg.from_user.id,
                                   f"Ученик: {padawan_full_name}\n"
                                   f"Группа: {a}\n"
                                   f"День занятий: {b}\n"
                                   f"Время занятий:{c}\n"
                                   f"Преподаватель:{d}\n\n"
                                   f"Поздравляю,ты дабавлен в свою группу.")

            await bot.send_message(msg.from_user.id,
                                   "Теперь для тебя открыты следующие функции:\n"
                                   "    1)Напоминание о выполнении домашнего задания\n"
                                   "    2)Напоминание о предстоящем уроке за день до\n"
                                   "    3)Я буду присылать тебе опрос после каждого урока, чтобы мы вместе становились лучше")

        working_with_json.json_change_flag_state(new_flag_state="  ",
                                                 telegram_username=msg["from"]["username"])

    b = datetime.datetime.now()
    print(b)


########################################################################################################################
# ОБРАБОТКА КНОПОК КЛАВИАТУРЫ

# добавление группы   ✅
@dp.callback_query_handler(text='event_add_group_button')
async def event_jedi_button(callback: types.CallbackQuery):
    global flag_new_group
    await callback.message.answer("Давай добавим новую группу по такому шаблону(одним сообщением):\n\n"
                                  "Название группы \nдень недели (по счету) \nвремя занятия\n"
                                  "номер последнего урока(М_У_\nназвание курса \n\nПример:\n\nNewmini2934_ПТ-18 "
                                  "\n5 \n18:00\nМ4У3\npython base")
    # Меняем состояние флага на Flag_new_group
    working_with_json.json_change_flag_state(telegram_username=callback["from"]["username"],
                                             new_flag_state="Flag_new_group")


# Просмотр статистики
@dp.callback_query_handler(text='event_show_stats_button')
async def event_jedi_button(callback: types.CallbackQuery):
    await callback.message.answer("Скоро здесь будет раздел со статистикой")
    await callback.message.answer("Верну тебя обратно:", reply_markup=keyboard.jedi_menu_keyboard_markup)


# Добавление ученика
@dp.callback_query_handler(text='event_padawan_button')
async def event_jedi_button(callback: types.CallbackQuery):
    await callback.message.answer("Хорошо. Для этого тебе необходимо ввести код авторизации, который тебе "
                                  "прислал преподаватель.\n Если его нет- напиши своему преподавателю, пожалуйста")
    # Создаем для данного ученика профиль в data2.json
    # меняем состояние ученика на "flag_add_padawan"
    working_with_json.json_add_padawan_state_data2(padawan_telegram_username=callback["from"]["username"],
                                                   flag_state="flag_add_padawan")








if __name__ == '__main__':
    executor.start_polling(dp)
