import json


# функция добавления нового преподавателя
def json_add_new_jedi(jedi_kodland_email=None, jedi_telegram_username=None, jedi_full_name=None):
    with open('data.JSON', 'r', encoding="utf-8") as f:
        json_data = json.load(f)

        add_pattern_jedi = {
            "full_name": f"{jedi_full_name}",
            "jedi_kodland_email": f"{jedi_kodland_email}",
            "padawans_groups": {}
        }

        json_data["jedi"][jedi_telegram_username] = add_pattern_jedi

    with open('data.JSON', 'w', encoding="utf-8") as f:
        f.write(json.dumps(json_data, ensure_ascii=False))
        f.close()

    with open('data2.JSON', 'r', encoding="utf-8") as f:
        json_data = json.load(f)

        add_pattern = {
            "flag_state": "",
            "status": "jedi",
            "mail_pin": ""
        }
        json_data["tg"][jedi_telegram_username] = add_pattern

    with open('data2.JSON', 'w', encoding="utf-8") as f:
        f.write(json.dumps(json_data, ensure_ascii=False))
        f.close()
    return True


# функция добавления новой группы
def json_add_new_group(group_name, auth_padawan_pin, lesson_day, lesson_time, number_last_lesson=None, course_name=None, jedi_telegram_username=None,):
    print("функция добавления новой группы")
    print(json_check(required_verification="group", jedi_telegram_username=jedi_telegram_username,
                      group_name=group_name))
    if not json_check(required_verification="group", jedi_telegram_username=jedi_telegram_username,
                      group_name=group_name):
        with open('data.JSON', 'r', encoding="utf-8") as f:
            json_data = json.load(f)

            add_pattern_group = {
                "group_data": {
                    "auth_padawan_pin": f"{auth_padawan_pin}",
                    "number_last_lesson": f"{number_last_lesson}",
                    "lesson_day": f"{lesson_day}",
                    "lesson_time": f"{lesson_time}",
                    "average_rating_all_padawans": "0",
                    "course_name": f"{course_name}"
                },
                "padawans": {}
            }
            json_data["jedi"][jedi_telegram_username]["padawans_groups"][group_name] = add_pattern_group
            print("Группа добавлена")
        with open('data.JSON', 'w', encoding="utf-8") as f:
            f.write(json.dumps(json_data, ensure_ascii=False))
            f.close()
        return True
    else:
        return True



# функция добавления нового ученика по пину
def json_add_new_padawan(padawan_telegram_username, auth_padawan_pin, padawan_full_name):
    input_group_name = json_group_find_pin(auth_padawan_pin)
    if input_group_name[0]:
        with open('data.JSON', 'r', encoding="utf-8") as f:
            json_data = json.load(f)
            add_pattern_padawan = {
                "name": f"{padawan_full_name}",
                "attendance": "0",
                "rating_lesson": {
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
            json_data["jedi"][input_group_name[2]]["padawans_groups"][input_group_name[1]]["padawans"][
                padawan_telegram_username] = add_pattern_padawan
        with open('data.JSON', 'w', encoding="utf-8") as f:
            f.write(json.dumps(json_data, ensure_ascii=False))
            f.close()
        return True, input_group_name[1]        #ученика не было, но мы его добавили
    else:
        return False, input_group_name[1]       #ученик уже есть, грузим для него стартовую клавиатуру





# функция проверки  Переписать ученика
def json_check(required_verification, jedi_kodland_email=None, jedi_telegram_username=None, jedi_full_name=None,
               group_name=None, padawan_telegram_username=None):
    # проверка на группу
    if required_verification == "group":
        try:

            with open('data.JSON', 'r', encoding="utf-8") as f:
                json_data = json.load(f)
                all_group = ""
                for i in json_data["jedi"][jedi_telegram_username]["padawans_groups"].keys():
                    all_group += i
                    print(i)

                if group_name in all_group:
                    return True
                else:
                    return False
        except KeyError:
            print("пустой список групп")
            return False

    # проверка  преподавателя (по нику телеграма)
    elif required_verification == "jedi":

        with open('data.JSON', 'r', encoding="utf-8") as f:
            json_data = json.load(f)
            all_jedi = ""
            for i in json_data["jedi"].keys():
                all_jedi += i

            if jedi_telegram_username in all_jedi:
                return True
            else:
                return False
    # проверка ученика (по нику телеграма)
    elif required_verification == "padawan":

        with open('data.JSON', 'r', encoding="utf-8") as f:
            json_data = json.load(f)
            all_padawans = ""
            for i in json_data["jedi"][jedi_telegram_username]["padawans_groups"][group_name]["padawans"].keys():
                all_padawans += i

            if padawan_telegram_username in all_padawans:
                return True
            else:
                return False


# Нахождение номера группы по pin-коду
def json_group_find_pin(auth_padawan_pin):
    with open('data.JSON', 'r', encoding="utf-8") as f:
        json_data = json.load(f)
        for jedi_telegram_username in json_data["jedi"].keys():
            for group_name in json_data["jedi"][jedi_telegram_username]["padawans_groups"].keys():
                if json_data["jedi"][jedi_telegram_username]["padawans_groups"][group_name]["group_data"][
                    "auth_padawan_pin"] == str(auth_padawan_pin):
                    return True, group_name, jedi_telegram_username

        return False, False


# Изменение состояния flag_state в data2
def json_change_flag_state(new_flag_state, telegram_username):
    with open('data2.JSON', 'r', encoding="utf-8") as f:
        json_data = json.load(f)
        json_data["tg"][str(telegram_username)]["flag_state"] = new_flag_state

    with open('data2.JSON', 'w', encoding="utf-8") as f:
        f.write(json.dumps(json_data, ensure_ascii=False))
        f.close()
    return True


# Чтение состояния flag_state в data2
def json_read_flag_state(telegram_username):
    with open('data2.JSON', 'r', encoding="utf-8") as f:
        json_data = json.load(f)
        f.close()
        return json_data["tg"][str(telegram_username)]["flag_state"]


# Изменение состояния mail_pin в data2
def json_change_mail_pin(new_mail_pin, telegram_username):
    with open('data2.JSON', 'r', encoding="utf-8") as f:
        json_data = json.load(f)
        json_data["tg"][telegram_username]["mail_pin"] = new_mail_pin

    with open('data2.JSON', 'w', encoding="utf-8") as f:
        f.write(json.dumps(json_data, ensure_ascii=False))
        f.close()
    return True


# Чтение состояния mail_pin в data2
def json_read_mail_pin(telegram_username):
    with open('data2.JSON', 'r', encoding="utf-8") as f:
        json_data = json.load(f)
        f.close()
        return json_data["tg"][telegram_username]["mail_pin"]


#функция добавления ученика в data2.json перед созданием его профиля в data.json
def json_add_padawan_state_data2(padawan_telegram_username,flag_state):
    with open('data2.JSON', 'r', encoding="utf-8") as f:
        json_data = json.load(f)

        add_pattern = {
            "flag_state": f"{flag_state}",
            "status": "padawan",
            "mail_pin": ""
        }
        json_data["tg"][padawan_telegram_username] = add_pattern

    with open('data2.JSON', 'w', encoding="utf-8") as f:
        f.write(json.dumps(json_data, ensure_ascii=False))
        f.close()










#Функция которая возвращает строчку окончания напоминаний
def date_calculation(range_course, mounth_last_lesson, num_last_lesson, lesson_day):
    import datetime
    now_week_num = datetime.datetime.today().isoweekday()  # из datetime хватаем номер дня сегодня
    # считаем сколько недель осталось учиться
    num_week = int(range_course) - int(mounth_last_lesson) * int(num_last_lesson)
    # считаем сколько это дней + разница до урока
    day_num = num_week * 7 + (int(lesson_day) - int(now_week_num))
    date = datetime.datetime.today().strftime("%m/%d/%y")
    date_1 = datetime.datetime.strptime(date, "%m/%d/%y")
    end_date = date_1 + datetime.timedelta(days=day_num)
    return end_date.strftime("%Y-%m-%d")



#функция изменения оценки
def rating_change(number_rating, padawan_id, rating_value):
    with open('data.JSON', 'r', encoding="utf-8") as f:
        json_data = json.load(f)
        for jedi_telegram_id in json_data["jedi"].keys():
            for group_name in json_data["jedi"][jedi_telegram_id]["padawans_groups"].keys():
                for id in json_data["jedi"][jedi_telegram_id]["padawans_groups"][group_name]["padawans"]:
                    if id == str(padawan_id):
                        rating_naw = json_data["jedi"][jedi_telegram_id]["padawans_groups"][group_name]["padawans"][id]["rating_lesson"][number_rating]
                        rating_naw = int(rating_naw) + int(rating_value)
                        json_data["jedi"][jedi_telegram_id]["padawans_groups"][group_name]["padawans"][id][
                            "rating_lesson"][number_rating] = str(rating_naw)
                        print(rating_naw)
                        break

    with open('data.JSON', 'w', encoding="utf-8") as f:
        f.write(json.dumps(json_data, ensure_ascii=False))
        f.close()



#функция изменения посещаемости
def attendance_change(padawan_id, attendance_value):
    with open('data.JSON', 'r', encoding="utf-8") as f:
        json_data = json.load(f)
        for jedi_telegram_id in json_data["jedi"].keys():
            for group_name in json_data["jedi"][jedi_telegram_id]["padawans_groups"].keys():
                for id in json_data["jedi"][jedi_telegram_id]["padawans_groups"][group_name]["padawans"]:
                    if id == str(padawan_id):
                        rating_naw = json_data["jedi"][jedi_telegram_id]["padawans_groups"][group_name]["padawans"][id]["attendance"]
                        rating_naw = int(rating_naw) + int(attendance_value)
                        json_data["jedi"][jedi_telegram_id]["padawans_groups"][group_name]["padawans"][id]["attendance"] = str(rating_naw)
                        print(rating_naw)
                        break

    with open('data.JSON', 'w', encoding="utf-8") as f:
        f.write(json.dumps(json_data, ensure_ascii=False))
        f.close()



