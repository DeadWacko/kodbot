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
import asyncio
import working_with_json
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

import json
from datetime import datetime

from loguru import logger

import datetime

logger.add("debag.log", format="{time} {level} {message}", level="DEBUG", compression="zip")

jobstores = {
    'default': SQLAlchemyJobStore(url='sqlite:///grou1p3.sqlite')
}

job_defaults = {
    'coalesce': False,
    'max_instances': 3
}

scheduler = AsyncIOScheduler(jobstores=jobstores, job_defaults=job_defaults, timezone="Europe/Moscow")
scheduler.start()

bot = Bot(token=token)
dp = Dispatcher(bot)

########################################################################################################################
#                       ТОЧНО РАБОТАЕТ И ИЗМЕНЕНИЯ НЕ ТРЕБУЮТСЯ

#   ОТПРАВКА ПИСЬМА НА ПОЧТУ
@logger.catch()
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

#   СТАРТОВАЯ КЛАВИАТУРА
@logger.catch()
@dp.message_handler(commands=['start'])
async def process_command_1(message: types.Message):
    await message.reply("Привет, выбери свой статус :3", reply_markup=keyboard.start_keyboard_markup)






########################################################################################################################


@logger.catch()
async def print_class_reminder(name_group: str):
    try:
        all_padawan = []
        jedi_telegram_id = ""
        group_name_ = ""
        time_group = ""
        lesson_num = ""
        with open('data.JSON', 'r', encoding="utf-8") as f:
            json_data = json.load(f)
            for jedi_telegram_id in json_data["jedi"].keys():
                for group_name in json_data["jedi"][jedi_telegram_id]["padawans_groups"].keys():
                    if group_name == str(name_group):
                        group_name_ = group_name
                        time_group = json_data["jedi"][jedi_telegram_id]["padawans_groups"][group_name]["group_data"][
                            "lesson_time"]
                        lesson_num = json_data["jedi"][jedi_telegram_id]["padawans_groups"][group_name]["group_data"][
                            "number_last_lesson"]

                        break

            for id in json_data["jedi"][jedi_telegram_id]["padawans_groups"][group_name_]["padawans"]:
                logger.success(f"Сообщение отправлено пользователю:_  {id}")
                await bot.send_message(int(id),
                                       f"⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠️\nПривет, через 24ч у тебя состоится урок в группе  {group_name_}.\n"
                                       f"Время урока: {time_group}\n"
                                       f"Номер урока:  {lesson_num}", reply_markup=keyboard.visitation_keyboard_markup)
    except:
        print("Нет учеников")
        logger.error("НЕТ УЧЕНИКОВ")


@logger.catch()
async def print_homework_reminder(name_group: str):
    try:
        all_padawan = []
        jedi_telegram_id = ""
        group_name_ = ""
        time_group = ""
        lesson_num = ""
        with open('data.JSON', 'r', encoding="utf-8") as f:
            json_data = json.load(f)
            for jedi_telegram_id in json_data["jedi"].keys():
                for group_name in json_data["jedi"][jedi_telegram_id]["padawans_groups"].keys():
                    if group_name == str(name_group):
                        group_name_ = group_name

                        break

            for id in json_data["jedi"][jedi_telegram_id]["padawans_groups"][group_name_]["padawans"]:
                logger.success(f"Сообщение отправлено пользователю:_  {id}")
                await bot.send_message(int(id),
                                       text="❗❗❗Привет, сегодня самое время приступить к выполнению домашнего задания, не забудь❗❗❗")
    except:
        print("Нет учеников")
        logger.error("НЕТ УЧЕНИКОВ")


@logger.catch()
async def print_notice_after_lesson(name_group: str):
    try:
        all_padawan = []
        jedi_telegram_id = ""
        group_name_ = ""
        time_group = ""
        lesson_num = ""
        with open('data.JSON', 'r', encoding="utf-8") as f:
            json_data = json.load(f)
            for jedi_telegram_id in json_data["jedi"].keys():
                for group_name in json_data["jedi"][jedi_telegram_id]["padawans_groups"].keys():
                    if group_name == str(name_group):
                        group_name_ = group_name

                        break

            for id in json_data["jedi"][jedi_telegram_id]["padawans_groups"][group_name_]["padawans"]:
                logger.success(f"Сообщение отправлено пользователю:_  {id}")
                await bot.send_message(int(id),
                                       text="Привет, расскажи пожалуйста,как прошел твой урок!\n Если конечно ты присутствовал сегодня")
                await bot.send_message(int(id),
                                       text="Первый вопрос, ты сегодня был на уроке?",
                                       reply_markup=keyboard.yes_no_keyboard_markup)
                working_with_json.json_change_flag_state(new_flag_state="Answer_1", telegram_username=id)
    except:
        print("Нет учеников")
        logger.error("НЕТ УЧЕНИКОВ")





# регистрация преподавателя
@logger.catch()
@dp.callback_query_handler(text='event_jedi_button')
async def event_jedi_button(callback: types.CallbackQuery):
    await callback.message.answer('Так, давай-ка я проверю, не заходил ли ты раньше,секундочку...')
    if not working_with_json.json_check(required_verification="jedi",
                                        jedi_telegram_username=str(callback.from_user.id)):
        await callback.message.answer('Ага, ты здесь впервые, давайка тебя добавим:3')
        await callback.message.answer('Секундочку, создаю для тебя директорию...')

        #
        #
        # Создаем пользователя(добавить шаблон для него, но без почты. для добавления почты необходима отдельная ф-я.
        #
        #
        working_with_json.json_add_new_jedi(jedi_telegram_username=str(callback["from"]["id"]))
        print(callback["from"]["id"])
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
                                                 telegram_username=str(callback.from_user.id))
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
@logger.catch()
async def input_text_msg(msg: types.Message):
    old_messadge = ""
    new_messedge = ""
    input_flag_state = working_with_json.json_read_flag_state(telegram_username=str(msg.from_user.id))
    print(input_flag_state)

    # ✅
    if input_flag_state == "Flag_mail":
        logger.success("Отправка кода на почту")
        new_messadge = msg.text
        if "@kodland.team" in new_messadge:
            await bot.send_message(msg.from_user.id, "Почта подходит,\n, секундочку...отправляю код")
            # создаем пин код`      ✅
            mail_pin = random.randint(100000, 999999)
            # отправляем код на почту      ✅
            send_mail("kodbot.mail@gmail.com", str(mail_pin))

            # добавляем код в date2.json    ✅
            working_with_json.json_change_mail_pin(new_mail_pin=mail_pin, telegram_username=str(msg.from_user.id))

            await bot.send_message(msg.from_user.id, "отправил код")

            old_messadge = new_messadge
            # меняем состояние флага преподавателя на flag_mail_pin     ✅
            working_with_json.json_change_flag_state(new_flag_state="flag_mail_pin",
                                                     telegram_username=str(msg.from_user.id))
            #
            #
            # Тут нужно добавить эту почту в json
            #
            #
            #
            #

            print(working_with_json.json_read_flag_state(telegram_username=str(msg.from_user.id)))

        else:
            await bot.send_message(msg.from_user.id, "ТЫ ШПИОН")
    # ✅
    elif input_flag_state == "flag_mail_pin":
        logger.success("Проверка пина с почты")
        ##############################################################
        # проверка pin-кода с почты                                  #
        ##############################################################

        new_messedge = msg.text  # ИЗБАВИТЬСЯ ОТ ЭТОГО БЕЗОБРАЗИЯ

        # меняем состояние флага преподавателя на " "          ✅
        working_with_json.json_change_flag_state(new_flag_state="  ",
                                                 telegram_username=str(msg.from_user.id))
        # читаем код с почты для авторизации почты ✅
        mail_pin = working_with_json.json_read_mail_pin(telegram_username=str(msg.from_user.id))
        if new_messedge == str(mail_pin):
            await bot.send_message(msg.from_user.id, "Готово,код подошел,я тебя проверил:3",
                                   reply_markup=keyboard.jedi_menu_keyboard_markup)

        # если подошел код - загружаем стартовую клавиатуру преподавателя ✅
        #
        old_messadge = new_messedge

    elif input_flag_state == "Flag_new_group":
        logger.success("Добавление новой группы")
        new_messedge = msg.text

        name_group = new_messedge.split("\n")[0]
        day_group = new_messedge.split("\n")[1]
        time_group = new_messedge.split("\n")[2]
        last_lesson_group = new_messedge.split("\n")[3]
        course_name_group = new_messedge.split("\n")[4]
        range_course = new_messedge.split("\n")[5]

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
                                             jedi_telegram_username=str(msg.from_user.id),
                                             auth_padawan_pin=group_auth_pin)
        mounth_last_lesson = last_lesson_group[1]
        num_last_lesson = last_lesson_group[3]
        # тут нужно установить напоминания для группы ( пока что хотя бы перед уроком)

        last_date = working_with_json.date_calculation(range_course=range_course, mounth_last_lesson=mounth_last_lesson,
                                                       num_last_lesson=num_last_lesson, lesson_day=day_group)

        logger.success(last_date)
        time_group = time_group.split(":")
        hours_group = time_group[0]
        minutes_group = time_group[1]
        logger.success(hours_group)

        day_name = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
        # Напоминание за 24ч об уроке
        scheduler.add_job(print_class_reminder, id=name_group, trigger='cron',
                          replace_existing=True, day_of_week=day_name[1], hour="22",
                          minute="32", args=(name_group,))
        # напоминание за 4 дня о выполнении дз
        name_group_2 = name_group + "_homework"
        scheduler.add_job(print_homework_reminder, id=name_group_2, trigger='cron',
                          replace_existing=True, day_of_week=day_name[1], hour="22",
                          minute="33", args=(name_group,))

        # напоминание после урока,чтобы его оценить
        name_group_3 = name_group + "_rating"
        scheduler.add_job(print_notice_after_lesson, id=name_group_3, trigger='cron',
                          replace_existing=True, day_of_week=day_name[1],
                          hour="22",
                          minute="35", args=(name_group,))
        scheduler._logger = logger

        await bot.send_message(msg.from_user.id, "Группа добавлена. Чтобы твои ученики смогли попасть в свою группу -"
                                                 f" передай им этот код авторизации\n\n\n {group_auth_pin}",
                               reply_markup=keyboard.jedi_menu_keyboard_markup)

        working_with_json.json_change_flag_state(new_flag_state="  ",
                                                 telegram_username=str(msg.from_user.id))


    elif input_flag_state == "flag_add_padawan":
        new_messedge = msg.text
        padawan_pin = new_messedge.split("\n")[0]

        padawan_full_name = new_messedge.split("\n")[1]

        answer_padawan = working_with_json.json_add_new_padawan(padawan_telegram_username=str(msg.from_user.id),
                                                                auth_padawan_pin=padawan_pin,
                                                                padawan_full_name=padawan_full_name)

        answer_flag = answer_padawan[0]

        answer_group_name = answer_padawan[1]

        week_day = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]

        a = "test"
        time_group = ""
        lesson_num = ""
        day_num = ""
        num_of_week = ""
        if answer_flag:
            with open('data.JSON', 'r', encoding="utf-8") as f:
                json_data = json.load(f)
                for jedi_telegram_id in json_data["jedi"].keys():
                    for group_name in json_data["jedi"][jedi_telegram_id]["padawans_groups"].keys():

                        if group_name == str(answer_group_name):
                            group_name = group_name
                            time_group = \
                                json_data["jedi"][jedi_telegram_id]["padawans_groups"][group_name]["group_data"][
                                    "lesson_time"]
                            lesson_num = \
                                json_data["jedi"][jedi_telegram_id]["padawans_groups"][group_name]["group_data"][
                                    "number_last_lesson"]
                            day_num = json_data["jedi"][jedi_telegram_id]["padawans_groups"][group_name]["group_data"][
                                "lesson_day"]
                            print(f"Время урока: {time_group}")
                            print(f"Номер урока: {lesson_num}")
                            print(f"День урока: {day_num}")
                            print(int(day_num))
                            break
            num_of_week = week_day[int(day_num) - 1]
            await bot.send_message(msg.from_user.id,
                                   text=f"Ученик: {padawan_full_name}\nГруппа: {answer_group_name}\nДень занятий: {num_of_week}\nВремя занятий:{time_group}\nПоследнее занятие: {lesson_num}\nПоздравляю,ты дабавлен в свою группу.")

            await bot.send_message(msg.from_user.id,
                                   "Теперь для тебя открыты следующие функции:\n"
                                   "    1)Напоминание о выполнении домашнего задания\n"
                                   "    2)Напоминание о предстоящем уроке за день до\n"
                                   "    3)Я буду присылать тебе опрос после каждого урока, чтобы мы вместе становились лучше")

        working_with_json.json_change_flag_state(new_flag_state="  ",
                                                 telegram_username=str(msg.from_user.id))

    print(msg)


########################################################################################################################
# ОБРАБОТКА КНОПОК КЛАВИАТУРЫ

# добавление группы   ✅
@logger.catch()
@dp.callback_query_handler(text='event_add_group_button')
async def event_jedi_button(callback: types.CallbackQuery):
    global flag_new_group
    await callback.message.answer("Давай добавим новую группу по такому шаблону(одним сообщением):\n\n"
                                  "Название группы \nдень недели (по счету) \nвремя занятия\n"
                                  "номер последнего урока(М_У_\nназвание курса \n\nПример:\n\nNewmini2934_ПТ-18 "
                                  "\n5 \n18:00\nМ4У3\npython base")
    # Меняем состояние флага на Flag_new_group
    working_with_json.json_change_flag_state(telegram_username=str(callback.from_user.id),
                                             new_flag_state="Flag_new_group")


# Просмотр статистики
@logger.catch()
@dp.callback_query_handler(text='event_show_stats_button')
async def event_jedi_button(callback: types.CallbackQuery):
    await callback.message.answer("Скоро здесь будет раздел со статистикой")
    await callback.message.answer("Верну тебя обратно:", reply_markup=keyboard.jedi_menu_keyboard_markup)


# Добавление ученика
@logger.catch()
@dp.callback_query_handler(text='event_padawan_button')
async def event_jedi_button(callback: types.CallbackQuery):
    await callback.message.answer("Хорошо. Для этого тебе необходимо ввести код авторизации, который тебе "
                                  "прислал преподаватель.\n Если его нет- напиши своему преподавателю, пожалуйста")
    # Создаем для данного ученика профиль в data2.json
    # меняем состояние ученика на "flag_add_padawan"
    working_with_json.json_add_padawan_state_data2(padawan_telegram_username=str(callback.from_user.id),
                                                   flag_state="flag_add_padawan")


# стартовая клавиатура
@logger.catch()
@dp.message_handler(commands=['start'])
async def process_command_1(message: types.Message):
    await message.reply("Привет, выбери свой статус :3", reply_markup=keyboard.start_keyboard_markup)


# регистрация преподавателя
@logger.catch()
@dp.callback_query_handler(text='event_jedi_button')
async def event_jedi_button(callback: types.CallbackQuery):
    await callback.message.answer('Так, давай-ка я проверю, не заходил ли ты раньше,секундочку...')
    if not working_with_json.json_check(required_verification="jedi",
                                        jedi_telegram_username=str(callback.from_user.id)):
        await callback.message.answer('Ага, ты здесь впервые, давайка тебя добавим:3')
        await callback.message.answer('Секундочку, создаю для тебя директорию...')

        #
        #
        # Создаем пользователя(добавить шаблон для него, но без почты. для добавления почты необходима отдельная ф-я.
        #
        #
        working_with_json.json_add_new_jedi(jedi_telegram_username=str(callback["from"]["id"]))
        print(callback["from"]["id"])
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
                                                 telegram_username=str(callback.from_user.id))
    else:
        await callback.message.answer('Ты уже есть, кыш атседа')
        await callback.message.answer('Вот тебе стартовая клавиатура преподавателя',
                                      reply_markup=keyboard.jedi_menu_keyboard_markup)


# Клавиатура (буду на уроке)
@logger.catch()
@dp.callback_query_handler(text='event_visit_button')
async def process_command_3(message: types.Message):
    pass


# Клавиатура (НЕ буду на уроке)
@logger.catch()
@dp.callback_query_handler(text='event_truancy_button')
async def process_command_4(callback: types.CallbackQuery):
    await callback.reply("Эхть, ну тогда ладно")


# Клавиатура ДА НЕТ
@logger.catch()
@dp.callback_query_handler(text='event_truancy_button')
async def process_command_5(callback: types.CallbackQuery):
    flag_state = working_with_json.json_read_flag_state(callback.from_user.id)
    # Туть мы спросили был ли ученик на уроке. Если был - кидаем остальные клавы. Если нет- то не кидаем
    if flag_state == "Answer_1":
        await callback.reply( reply_markup=keyboard.rate_lesson_keyboard_markup)
        working_with_json.json_change_flag_state(new_flag_state="Answer_yes", telegram_username=id)




# Клавиатура one
@logger.catch()
@dp.callback_query_handler(text='one')
async def rating_one(callback: types.CallbackQuery):
    flag_state = working_with_json.json_read_flag_state(callback.from_user.id)
    # Туть мы спросили был ли ученик на уроке. Если был - кидаем остальные клавы. Если нет- то не кидаем
    if flag_state == "Answer_yes":
        #меняем рейтинг в первом опросе на 1
        working_with_json.rating_change(number_rating="1", padawan_id=callback.from_user.id, rating_value=1)
        await callback.message.edit_reply_markup(reply_markup=keyboard.rate_work_keyboard_markup)
        working_with_json.json_change_flag_state(new_flag_state="Answer_one_2", telegram_username=id)
    elif flag_state == "Answer_one_2":
        working_with_json.rating_change(number_rating="2", padawan_id=callback.from_user.id, rating_value=1)
        await callback.message.edit_reply_markup(reply_markup=keyboard.rate_explanations_keyboard_markup)
        working_with_json.json_change_flag_state(new_flag_state="Answer_one_3", telegram_username=id)
    elif flag_state == "Answer_one_3":
        working_with_json.rating_change(number_rating="3", padawan_id=callback.from_user.id, rating_value=1)
        await callback.message.edit_reply_markup(reply_markup=keyboard.rate_skill_keyboard_markup)
        working_with_json.json_change_flag_state(new_flag_state="Answer_one_4", telegram_username=id)

    elif flag_state == "Answer_one_3":
        working_with_json.rating_change(number_rating="4", padawan_id=callback.from_user.id, rating_value=1)
        await callback.message.edit_reply_markup(reply_markup=keyboard.problems_keyboard_markup)
        working_with_json.json_change_flag_state(new_flag_state="Answer_one_5", telegram_username=id)







        #todo    Сделать добавление оценки в json файл
        #        отправить следующий опрос









if __name__ == '__main__':
    executor.start_polling(dp)
    scheduler.start()
    asyncio.get_event_loop().run_forever()
