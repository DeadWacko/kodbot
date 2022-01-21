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
logger.success("БОТ СТАРТАНУЛ")










########################################################################################################################
#                                        НАПОМИНАНИЯ

#   ТОЧНО РАБОТАЕТ
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


#   ТОЧНО РАБОТАЕТ
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
        jedi_telegram_id = ""
        group_name_ = ""
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








########################################################################################################################
#                       ТОЧНО РАБОТАЕТ И ИЗМЕНЕНИЯ НЕ ТРЕБУЮТСЯ

#   ОТПРАВКА ПИСЬМА НА ПОЧТУ
@logger.catch()
def send_mail(input_mail, send_pin):
    fromaddr = 'kodbot.mail@gmail.com'
    toaddrs = input_mail
    # Writing the message (this message will appear in the email)
    msg = f"Privet, tvoj kod dlya avtorizacii prepodavatelya. Vvedi ego pozhalujsta v soobshcheniya botu. Priyatnogo pol'zovaniya  {send_pin}"
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
    logger.debug(f"пользователь {message.from_user.id} Нажал стартовую клавиатуру")
    logger.success("Нажали старт")
    await message.reply("Привет, выбери свой статус :3", reply_markup=keyboard.start_keyboard_markup)


#   ДОБАВЛЕНИЕ ГРУППЫ
@logger.catch()
@dp.callback_query_handler(text='event_add_group_button')
async def event_jedi_button(callback: types.CallbackQuery):
    global flag_new_group
    await callback.message.answer("Давай добавим новую группу по такому шаблону(одним сообщением):\n\n"
                                  "Название группы \nдень недели (по счету) \nвремя занятия\n"
                                  "номер последнего урока(М_У_\nназвание курса \n\nПример:\n\nNewmini2934_ПТ-18 "
                                  "\n5 \n18:00\nМ4У3\npython base")
    working_with_json.json_change_flag_state(telegram_username=str(callback.from_user.id),
                                             new_flag_state="Flag_new_group")
    logger.success(f"Преподаватель {callback.from_user.id} добавляет группу")


# ПРОСМОТР СТАТИСТИКИ ( ПОДГРУЖАТЬ ТУДА ПОСЛЕ НОРМАЛЬНУЮ КЛАВИАТУРУ)
@logger.catch()
@dp.callback_query_handler(text='event_show_stats_button')
async def event_jedi_button(callback: types.CallbackQuery):
    await callback.message.answer("Скоро здесь будет раздел со статистикой")
    await callback.message.answer("Верну тебя обратно:", reply_markup=keyboard.jedi_menu_keyboard_markup)


#   РЕГИСТРАЦИЯ ПРЕПОДАВАТЕЛЯ
@logger.catch()
@dp.callback_query_handler(text='event_jedi_button')
async def event_jedi_button(callback: types.CallbackQuery):
    logger.success(f"Преподаватель {callback.from_user.id} регистрируется")
    await callback.message.answer('Так, давай-ка я проверю, не заходил ли ты раньше,секундочку...')
    if not working_with_json.json_check(required_verification="jedi",
                                        jedi_telegram_username=str(callback.from_user.id)):
        await callback.message.answer('Ага, ты здесь впервые, давайка тебя добавим:3')
        await callback.message.answer('Секундочку, создаю для тебя директорию...')
        working_with_json.json_add_new_jedi(jedi_telegram_username=str(callback["from"]["id"]))
        print(callback["from"]["id"])
        await callback.message.answer(
            'Готово.\n Но теперь давай проверим тебя. Введи свою корпоративную почту, я вышлю тебе код.\n'
            'П.с. у тебя будет всего 5 попыток, после этого я удалю тебя :с')

        working_with_json.json_change_flag_state(new_flag_state="Flag_mail",
                                                 telegram_username=str(callback.from_user.id))
    else:
        await callback.message.answer('Ты уже есть, кыш атседа')
        await callback.message.answer('Вот тебе стартовая клавиатура преподавателя',
                                      reply_markup=keyboard.jedi_menu_keyboard_markup)


#   ДОБАВЛЕНИЕ УЧЕНИКА
@logger.catch()
@dp.callback_query_handler(text='event_padawan_button')
async def event_jedi_button(callback: types.CallbackQuery):
    logger.success(f"Ученик {callback.from_user.id} Вводит код")
    await callback.message.answer("Хорошо. Для этого тебе необходимо ввести код авторизации, который тебе "
                                  "прислал преподаватель.\n Если его нет- напиши своему преподавателю, пожалуйста\n"
                                  "Формат ввода:\n"
                                  "Код\n"
                                  "Фамилия Имя\n\n"
                                  "Пример:\n"
                                  "394321\n"
                                  "Костюкевич Михаил")
    # Создаем для данного ученика профиль в data2.json
    # меняем состояние ученика на "flag_add_padawan"
    working_with_json.json_add_padawan_state_data2(padawan_telegram_username=str(callback.from_user.id),
                                                   flag_state="flag_add_padawan")
    logger.success(f"Смена статуса ученика {callback.from_user.id} произведена на flag_add_padawan")


########################################################################################################################
# ответы на текстовые сообщения
@dp.message_handler()
@logger.catch()
async def input_text_msg(msg: types.Message):
    logger.success(f"Пришло сообщение от пользователя {msg.from_user.id}")
    logger.success(f"{msg.text}")
    logger.success(f"Сообщение от пользователя {msg.from_user.id} Обрабатывается")
    old_messadge = ""
    new_messedge = ""
    input_flag_state = working_with_json.json_read_flag_state(telegram_username=str(msg.from_user.id))

    # ✅
    if input_flag_state == "Flag_mail":
        logger.success("Отправка кода на почту")
        new_messadge = msg.text
        if "@kodland.team" in new_messadge:
            await bot.send_message(msg.from_user.id, "Почта подходит,\n, секундочку...отправляю код")
            # создаем пин код`      ✅
            mail_pin = random.randint(100000, 999999)
            # отправляем код на почту      ✅
            send_mail(input_mail=new_messadge, send_pin=str(mail_pin))

            # добавляем код в date2.json    ✅
            working_with_json.json_change_mail_pin(new_mail_pin=mail_pin, telegram_username=str(msg.from_user.id))

            await bot.send_message(msg.from_user.id, "отправил код")
            logger.success(f"Код авторизации: {mail_pin} отправлен на почту {new_messadge}  пользователю {msg.from_user.id}")

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
        logger.success(f"Напоминание за 24ч для группы: {name_group} Создано. Время: {hours_group}  День: {int(day_group) - 2}")
        scheduler.add_job(print_class_reminder, id=name_group, trigger='cron',
                          replace_existing=True, day_of_week=day_name[int(day_group) - 2], hour=str(hours_group),
                          minute="0", args=(name_group,))
        # напоминание за 4 дня о выполнении дз
        logger.success(f"Напоминание за 4 дня для группы: {name_group} Создано. Время: {hours_group}  День: {int(day_group) - 5}")
        name_group_2 = name_group + "_homework"
        scheduler.add_job(print_homework_reminder, id=name_group_2, trigger='cron',
                          replace_existing=True, day_of_week=day_name[int(day_group) - 5], hour="17",
                          minute="0", args=(name_group,))

        # напоминание после урока,чтобы его оценить
        logger.success(f"Напоминание после урока для группы: {name_group} Создано. Время: {str(int(hours_group) + 1)}  День: {int(day_group) - 1}")
        name_group_3 = name_group + "_rating"
        scheduler.add_job(print_notice_after_lesson, id=name_group_3, trigger='cron',
                          replace_existing=True, day_of_week=day_name[int(day_group) - 1],
                          hour=str(int(hours_group) + 1),
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
            logger.success(f"Ученик: {padawan_full_name} Группа: {answer_group_name} День занятий: {num_of_week}Время занятий:{time_group} Последнее занятие: {lesson_num} дабавлен в свою группу.")
            await bot.send_message(msg.from_user.id,
                                   "Теперь для тебя открыты следующие функции:\n"
                                   "    1)Напоминание о выполнении домашнего задания\n"
                                   "    2)Напоминание о предстоящем уроке за день до\n"
                                   "    3)Я буду присылать тебе опрос после каждого урока, чтобы мы вместе становились лучше")

        working_with_json.json_change_flag_state(new_flag_state="  ",
                                                 telegram_username=str(msg.from_user.id))


    elif input_flag_state == "problems_add":
        new_messadge = msg.text
        # Обработка проблем ученика

        with open('data.JSON', 'r', encoding="utf-8") as f:
            json_data = json.load(f)
            for jedi_telegram_username in json_data["jedi"].keys():
                for group_name in json_data["jedi"][jedi_telegram_username]["padawans_groups"].keys():
                    for id in json_data["jedi"][jedi_telegram_username]["padawans_groups"][group_name]["padawans"]:
                        if str(id) == str(msg.from_user.id):
                            name = json_data["jedi"][jedi_telegram_username]["padawans_groups"][group_name]["padawans"][str(id)][
                                "name"]
                            break

        messedge = f"У твоего ученика из группы: {group_name} есть какие-то проблемы, помоги ему пожалуйста :сс\n\n" \
                   f"\n Вот что пишет  {name}:\n" + msg.text
        await bot.send_message(msg.from_user.id, "Готово, сообщение отправлено преподавателю!)")
        await bot.send_message(jedi_telegram_username, messedge)

        working_with_json.json_change_flag_state(new_flag_state=" ", telegram_username=str(msg.from_user.id))
        old_messadge = new_messadge

    else:
        await bot.send_message(msg.from_user.id, text="Неа,у тебя пока что нет поводов писать мне, увы :с")

#   КНОПКА ДА
@logger.catch()
@dp.callback_query_handler(text='event_yes_button')
async def yes_button(callback: types.CallbackQuery):
    logger.success(f"Нажата кнопка ДА пользователем {callback.from_user.id}")
    # добавляем ученику +1 в посещаемость +
    working_with_json.attendance_change(padawan_id=callback.from_user.id, attendance_value=1)
    #
    #
    # меняем состояние ученика на access_to_the_survey - доступ к опросу +
    working_with_json.json_change_flag_state(new_flag_state="access_to_the_survey",
                                             telegram_username=callback.from_user.id)
    #
    #
    # отправляем первый вопрос и клавиатуру к нему +
    await callback.message.answer(text="Как прошел сегодняшний урок?",
                                  reply_markup=keyboard.rate_lesson_keyboard_markup)


#   КНОПКА НЕТ
@logger.catch()
@dp.callback_query_handler(text='event_no_button')
async def yes_button(callback: types.CallbackQuery):
    await callback.answer(text="ЭХХХХХХХ, постарайся в следующий раз не прогуливать!(")
    logger.success(f"Нажата кнопка НЕТ пользователем {callback.from_user.id}")



# кнопка 1
@logger.catch()
@dp.callback_query_handler(text='one')
async def button_reting_1(callback: types.CallbackQuery):
    logger.success(f"Нажата кнопка one пользователем {callback.from_user.id}")
    reting = 1
    # записываем в переменную последнее состояние пользователя
    user_state = working_with_json.json_read_flag_state(telegram_username=callback.from_user.id)
    if user_state == "access_to_the_survey":
        # добавляем 1 в рейтинг №1           +
        working_with_json.rating_change(number_rating="1", padawan_id=callback.from_user.id, rating_value=reting)
        # меняем flag_state ученика на access_to_second_question +
        working_with_json.json_change_flag_state(new_flag_state="access_to_second_question",
                                                 telegram_username=callback.from_user.id)
        # отправляем следующий вопрос +
        await callback.message.answer(
            text="Как ты думаешь, ты хорошо сегодня поработал? как ты оцениваешь себя на уроке ?",
            reply_markup=keyboard.rate_work_keyboard_markup)
    elif user_state == "access_to_second_question":
        # добавляем 1 в рейтинг №2
        working_with_json.rating_change(number_rating="2", padawan_id=callback.from_user.id, rating_value=reting)
        # меняем flag_state ученика на access_to_third_question
        working_with_json.json_change_flag_state(new_flag_state="access_to_third_question",
                                                 telegram_username=callback.from_user.id)
        # отправляем следующий вопрос
        await callback.message.answer(
            text="Насколько хорошо ты понял объяснения преподавателя?",
            reply_markup=keyboard.rate_explanations_keyboard_markup)
    elif user_state == "access_to_third_question":
        # добавляем 1 в рейтинг №3
        working_with_json.rating_change(number_rating="3", padawan_id=callback.from_user.id, rating_value=reting)
        # меняем flag_state ученика на access_to_fourth_question
        working_with_json.json_change_flag_state(new_flag_state="access_to_fourth_question",
                                                 telegram_username=callback.from_user.id)
        # отправляем следующий вопрос
        await callback.message.answer(
            text="Как ты оцениваешь свои навыки программирования на сегодняшний день?",
            reply_markup=keyboard.rate_skill_keyboard_markup)
    elif user_state == "access_to_fourth_question":
        # добавляем 1 в рейтинг №4
        working_with_json.rating_change(number_rating="4", padawan_id=callback.from_user.id, rating_value=reting)

        # меняем flag_state ученика на пустуб строчку
        working_with_json.json_change_flag_state(new_flag_state="problems",
                                                 telegram_username=callback.from_user.id)
        # отправляем следующий вопрос
        await callback.message.answer(
            text="были ли какие-то проблемы?Если да, жамкай кнопку, я передам об этом преподавателю в понедельник",
            reply_markup=keyboard.problems_keyboard_markup)
    else:
        # Сказать что он уже нажимал на эту кнопку отправив уведомление
        await callback.answer("Неа,сюда ты уже нажимал",slow_alert = True)


# кнопка 2
@logger.catch()
@dp.callback_query_handler(text='two')
async def button_reting_2(callback: types.CallbackQuery):
    logger.success(f"Нажата кнопка two пользователем {callback.from_user.id}")
    reting = 2
    # записываем в переменную последнее состояние пользователя
    user_state = working_with_json.json_read_flag_state(telegram_username=callback.from_user.id)
    if user_state == "access_to_the_survey":
        # добавляем 1 в рейтинг №1           +
        working_with_json.rating_change(number_rating="1", padawan_id=callback.from_user.id, rating_value=reting)
        # меняем flag_state ученика на access_to_second_question +
        working_with_json.json_change_flag_state(new_flag_state="access_to_second_question",
                                                 telegram_username=callback.from_user.id)
        # отправляем следующий вопрос +
        await callback.message.answer(
            text="Как ты думаешь, ты хорошо сегодня поработал? как ты оцениваешь себя на уроке ?",
            reply_markup=keyboard.rate_work_keyboard_markup)
    elif user_state == "access_to_second_question":
        # добавляем 1 в рейтинг №2
        working_with_json.rating_change(number_rating="2", padawan_id=callback.from_user.id, rating_value=reting)
        # меняем flag_state ученика на access_to_third_question
        working_with_json.json_change_flag_state(new_flag_state="access_to_third_question",
                                                 telegram_username=callback.from_user.id)
        # отправляем следующий вопрос
        await callback.message.answer(
            text="Насколько хорошо ты понял объяснения преподавателя?",
            reply_markup=keyboard.rate_explanations_keyboard_markup)
    elif user_state == "access_to_third_question":
        # добавляем 1 в рейтинг №3
        working_with_json.rating_change(number_rating="3", padawan_id=callback.from_user.id, rating_value=reting)
        # меняем flag_state ученика на access_to_fourth_question
        working_with_json.json_change_flag_state(new_flag_state="access_to_fourth_question",
                                                 telegram_username=callback.from_user.id)
        # отправляем следующий вопрос
        await callback.message.answer(
            text="Как ты оцениваешь свои навыки программирования на сегодняшний день?",
            reply_markup=keyboard.rate_skill_keyboard_markup)
    elif user_state == "access_to_fourth_question":
        # добавляем 1 в рейтинг №4
        working_with_json.rating_change(number_rating="4", padawan_id=callback.from_user.id, rating_value=reting)

        # меняем flag_state ученика на пустуб строчку
        working_with_json.json_change_flag_state(new_flag_state="problems",
                                                 telegram_username=callback.from_user.id)
        # отправляем следующий вопрос
        await callback.message.answer(
            text="были ли какие-то проблемы?Если да, жамкай кнопку, я передам об этом преподавателю в понедельник",
            reply_markup=keyboard.problems_keyboard_markup)
    else:
        # Сказать что он уже нажимал на эту кнопку отправив уведомление
        await callback.answer("Неа,сюда ты уже нажимал",slow_alert = True)


# кнопка 3
@logger.catch()
@dp.callback_query_handler(text='three')
async def button_reting_3(callback: types.CallbackQuery):
    logger.success(f"Нажата кнопка three пользователем {callback.from_user.id}")
    reting = 3
    # записываем в переменную последнее состояние пользователя
    user_state = working_with_json.json_read_flag_state(telegram_username=callback.from_user.id)
    if user_state == "access_to_the_survey":
        # добавляем 1 в рейтинг №1           +
        working_with_json.rating_change(number_rating="1", padawan_id=callback.from_user.id, rating_value=reting)
        # меняем flag_state ученика на access_to_second_question +
        working_with_json.json_change_flag_state(new_flag_state="access_to_second_question",
                                                 telegram_username=callback.from_user.id)
        # отправляем следующий вопрос +
        await callback.message.answer(
            text="Как ты думаешь, ты хорошо сегодня поработал? как ты оцениваешь себя на уроке ?",
            reply_markup=keyboard.rate_work_keyboard_markup)
    elif user_state == "access_to_second_question":
        # добавляем 1 в рейтинг №2
        working_with_json.rating_change(number_rating="2", padawan_id=callback.from_user.id, rating_value=reting)
        # меняем flag_state ученика на access_to_third_question
        working_with_json.json_change_flag_state(new_flag_state="access_to_third_question",
                                                 telegram_username=callback.from_user.id)
        # отправляем следующий вопрос
        await callback.message.answer(
            text="Насколько хорошо ты понял объяснения преподавателя?",
            reply_markup=keyboard.rate_explanations_keyboard_markup)
    elif user_state == "access_to_third_question":
        # добавляем 1 в рейтинг №3
        working_with_json.rating_change(number_rating="3", padawan_id=callback.from_user.id, rating_value=reting)
        # меняем flag_state ученика на access_to_fourth_question
        working_with_json.json_change_flag_state(new_flag_state="access_to_fourth_question",
                                                 telegram_username=callback.from_user.id)
        # отправляем следующий вопрос
        await callback.message.answer(
            text="Как ты оцениваешь свои навыки программирования на сегодняшний день?",
            reply_markup=keyboard.rate_skill_keyboard_markup)
    elif user_state == "access_to_fourth_question":
        # добавляем 1 в рейтинг №4
        working_with_json.rating_change(number_rating="4", padawan_id=callback.from_user.id, rating_value=reting)

        # меняем flag_state ученика на пустуб строчку
        working_with_json.json_change_flag_state(new_flag_state="problems",
                                                 telegram_username=callback.from_user.id)
        # отправляем следующий вопрос
        await callback.message.answer(
            text="были ли какие-то проблемы?Если да, жамкай кнопку, я передам об этом преподавателю в понедельник",
            reply_markup=keyboard.problems_keyboard_markup)
    else:
        # Сказать что он уже нажимал на эту кнопку отправив уведомление
        await callback.answer("Неа,сюда ты уже нажимал",slow_alert = True)


# кнопка 4
@logger.catch()
@dp.callback_query_handler(text='four')
async def button_reting_4(callback: types.CallbackQuery):
    logger.success(f"Нажата кнопка four пользователем {callback.from_user.id}")
    reting = 4
    # записываем в переменную последнее состояние пользователя
    user_state = working_with_json.json_read_flag_state(telegram_username=callback.from_user.id)
    if user_state == "access_to_the_survey":
        # добавляем 1 в рейтинг №1           +
        working_with_json.rating_change(number_rating="1", padawan_id=callback.from_user.id, rating_value=reting)
        # меняем flag_state ученика на access_to_second_question +
        working_with_json.json_change_flag_state(new_flag_state="access_to_second_question",
                                                 telegram_username=callback.from_user.id)
        # отправляем следующий вопрос +
        await callback.message.answer(
            text="Как ты думаешь, ты хорошо сегодня поработал? как ты оцениваешь себя на уроке ?",
            reply_markup=keyboard.rate_work_keyboard_markup)
    elif user_state == "access_to_second_question":
        # добавляем 1 в рейтинг №2
        working_with_json.rating_change(number_rating="2", padawan_id=callback.from_user.id, rating_value=reting)
        # меняем flag_state ученика на access_to_third_question
        working_with_json.json_change_flag_state(new_flag_state="access_to_third_question",
                                                 telegram_username=callback.from_user.id)
        # отправляем следующий вопрос
        await callback.message.answer(
            text="Насколько хорошо ты понял объяснения преподавателя?",
            reply_markup=keyboard.rate_explanations_keyboard_markup)
    elif user_state == "access_to_third_question":
        # добавляем 1 в рейтинг №3
        working_with_json.rating_change(number_rating="3", padawan_id=callback.from_user.id, rating_value=reting)
        # меняем flag_state ученика на access_to_fourth_question
        working_with_json.json_change_flag_state(new_flag_state="access_to_fourth_question",
                                                 telegram_username=callback.from_user.id)
        # отправляем следующий вопрос
        await callback.message.answer(
            text="Как ты оцениваешь свои навыки программирования на сегодняшний день?",
            reply_markup=keyboard.rate_skill_keyboard_markup)
    elif user_state == "access_to_fourth_question":
        # добавляем 1 в рейтинг №4
        working_with_json.rating_change(number_rating="4", padawan_id=callback.from_user.id, rating_value=reting)

        # меняем flag_state ученика на пустуб строчку
        working_with_json.json_change_flag_state(new_flag_state="problems",
                                                 telegram_username=callback.from_user.id)
        # отправляем следующий вопрос
        await callback.message.answer(
            text="были ли какие-то проблемы?Если да, жамкай кнопку, я передам об этом преподавателю в понедельник",
            reply_markup=keyboard.problems_keyboard_markup)
    else:
        # Сказать что он уже нажимал на эту кнопку отправив уведомление
        await callback.answer("Неа,сюда ты уже нажимал",slow_alert = True)


# кнопка 5
@logger.catch()
@dp.callback_query_handler(text='five')
async def button_reting_5(callback: types.CallbackQuery):
    logger.success(f"Нажата кнопка five пользователем {callback.from_user.id}")
    reting = 5
    # записываем в переменную последнее состояние пользователя
    user_state = working_with_json.json_read_flag_state(telegram_username=callback.from_user.id)
    if user_state == "access_to_the_survey":
        # добавляем 1 в рейтинг №1           +
        working_with_json.rating_change(number_rating="1", padawan_id=callback.from_user.id, rating_value=reting)
        # меняем flag_state ученика на access_to_second_question +
        working_with_json.json_change_flag_state(new_flag_state="access_to_second_question",
                                                 telegram_username=callback.from_user.id)
        # отправляем следующий вопрос +
        await callback.message.answer(
            text="Как ты думаешь, ты хорошо сегодня поработал? как ты оцениваешь себя на уроке ?",
            reply_markup=keyboard.rate_work_keyboard_markup)
    elif user_state == "access_to_second_question":
        # добавляем 1 в рейтинг №2
        working_with_json.rating_change(number_rating="2", padawan_id=callback.from_user.id, rating_value=reting)
        # меняем flag_state ученика на access_to_third_question
        working_with_json.json_change_flag_state(new_flag_state="access_to_third_question",
                                                 telegram_username=callback.from_user.id)
        # отправляем следующий вопрос
        await callback.message.answer(
            text="Насколько хорошо ты понял объяснения преподавателя?",
            reply_markup=keyboard.rate_explanations_keyboard_markup)
    elif user_state == "access_to_third_question":
        # добавляем 1 в рейтинг №3
        working_with_json.rating_change(number_rating="3", padawan_id=callback.from_user.id, rating_value=reting)
        # меняем flag_state ученика на access_to_fourth_question
        working_with_json.json_change_flag_state(new_flag_state="access_to_fourth_question",
                                                 telegram_username=callback.from_user.id)
        # отправляем следующий вопрос
        await callback.message.answer(
            text="Как ты оцениваешь свои навыки программирования на сегодняшний день?",
            reply_markup=keyboard.rate_skill_keyboard_markup)
    elif user_state == "access_to_fourth_question":
        # добавляем 1 в рейтинг №4
        working_with_json.rating_change(number_rating="4", padawan_id=callback.from_user.id, rating_value=reting)

        # меняем flag_state ученика на пустуб строчку
        working_with_json.json_change_flag_state(new_flag_state="problems",
                                                 telegram_username=callback.from_user.id)
        # отправляем следующий вопрос
        await callback.message.answer(
            text="были ли какие-то проблемы?Если да, жамкай кнопку, я передам об этом преподавателю в понедельник",
            reply_markup=keyboard.problems_keyboard_markup)
    else:
        # Сказать что он уже нажимал на эту кнопку отправив уведомление
        await callback.answer("Неа,сюда ты уже нажимал")


# Кнопка ЕСТЬ ПРОБЛЕМЫ
@logger.catch()
@dp.callback_query_handler(text='event_problems_button')
async def button_reting_6(callback: types.CallbackQuery):
    logger.success(f"Нажата кнопка ЕСТЬ ПРОБЛЕМЫ пользователем {callback.from_user.id}")
    await callback.message.answer(
        text="Так-так-так, давай-ка я помогу тебе, опиши свою проблему, а я отправлю ее преподавателю в понедельник и он ответит тебе")
    working_with_json.json_change_flag_state(new_flag_state="problems_add", telegram_username=callback.from_user.id)


# Кнопка НЕТ ПРОБЛЕМ
@logger.catch()
@dp.callback_query_handler(text='event_no_problems_button')
async def button_reting_7(callback: types.CallbackQuery):
    logger.success(f"Нажата кнопка НЕТ ПРОБЛЕМ пользователем {callback.from_user.id}")
    await callback.message.answer(
        text="Какой(аяяя) же ты умничка:3\n Продолжай в том же духе *-*\n П.С. Ты крутышка:3")


if __name__ == '__main__':
    executor.start_polling(dp)
    scheduler.start()
    asyncio.get_event_loop().run_forever()
