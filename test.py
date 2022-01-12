import json


# функция добавления нового преподавателя
def json_add_new_jedi(jedi_kodland_email=None, jedi_telegram_username=None, jedi_full_name=None):
    with open('data.JSON', 'r', encoding="utf-8") as f:
        json_data = json.load(f)

        add_pattern_jedi = {
            "full_name": f"{jedi_full_name}",
            "jedi_kodland_email": f"{jedi_kodland_email}",
            "podawans_groups": {}
        }

        json_data["jedi"][jedi_telegram_username] = add_pattern_jedi

    with open('data.JSON', 'w', encoding="utf-8") as f:
        f.write(json.dumps(json_data, ensure_ascii=False))
        f.close()

    with open('data2.JSON', 'r', encoding="utf-8") as f:
        json_data = json.load(f)

        add_pattern = {
            "flag_state": "",
            "status": "jedi"
        }
        json_data["tg"][jedi_telegram_username] = add_pattern

    with open('data2.JSON', 'w', encoding="utf-8") as f:
        f.write(json.dumps(json_data, ensure_ascii=False))
        f.close()
    return True


# функция добавления новой группы
def json_add_new_group(group_name, lesson_day, lesson_time, number_last_lesson, course_name, jedi_telegram_username,
                       auth_padawan_pin):
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
        with open('data.JSON', 'w', encoding="utf-8") as f:
            f.write(json.dumps(json_data, ensure_ascii=False))
            f.close()
        return True
    else:
        return True


# функция добавления нового ученика по пину
def json_add_new_padawan(padawan_telegram_username, auth_padawan_pin, padawan_full_name):
    input_group_name = json_group_find_pin(auth_padawan_pin)
    with open('data.JSON', 'r', encoding="utf-8") as f:
        json_data = json.load(f)
        add_pattern_padawan = {
            "name": f"{padawan_full_name}",
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
        json_data["jedi"][input_group_name[2]]["padawans_groups"][input_group_name[1]]["padawans"][
            padawan_telegram_username] = add_pattern_padawan
    with open('data.JSON', 'w', encoding="utf-8") as f:
        f.write(json.dumps(json_data, ensure_ascii=False))
        f.close()

    with open('data2.JSON', 'r', encoding="utf-8") as f:
        json_data = json.load(f)

        add_pattern = {
            "flag_state": "",
            "status": "padawan"
        }
        json_data["tg"][padawan_telegram_username] = add_pattern

    with open('data2.JSON', 'w', encoding="utf-8") as f:
        f.write(json.dumps(json_data, ensure_ascii=False))
        f.close()
    return True


# функция проверки  Переписать ученика
def json_check(required_verification, jedi_kodland_email=None, jedi_telegram_username=None, jedi_full_name=None,
               group_name=None, padawan_telegram_username=None):
    # проверка на группу
    if required_verification == "group":

        with open('data.JSON', 'r', encoding="utf-8") as f:
            json_data = json.load(f)
            all_group = ""
            for i in json_data["jedi"][jedi_telegram_username]["padawans_groups"].keys():
                all_group += i

            if group_name in all_group:
                return True
            else:
                return False

    # проверка на преподавателя (по нику телеграма)
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
                    break
        return False, False





# Чтение групп у преподавателя
def json_read_group_list(jedi_telegram_username):
    with open('data.JSON', 'r', encoding="utf-8") as f:
        json_data = json.load(f)
        return json_data["jedi"][jedi_telegram_username]["padawans_groups"].keys()


# Чтение учеников в группе
def json_read_padawans_list(jedi_telegram_username, group_name):
    with open('data.JSON', 'r', encoding="utf-8") as f:
        json_data = json.load(f)
        return json_data["jedi"][jedi_telegram_username]["padawans_groups"][group_name]["padawans"].keys()


# Чтение состояния flag_state в data2
def json_read_flag_state(telegram_username):
    with open('data2.JSON', 'r', encoding="utf-8") as f:
        json_data = json.load(f)
        return json_data["tg"][telegram_username]["flag_state"]


# Изменение состояния flag_state в data2
def json_change_flag_state(new_flag_state, telegram_username):
    with open('data2.JSON', 'r', encoding="utf-8") as f:
        json_data = json.load(f)
        json_data["tg"][telegram_username]["flag_state"] = new_flag_state

    with open('data2.JSON', 'w', encoding="utf-8") as f:
        f.write(json.dumps(json_data, ensure_ascii=False))
        f.close()
    return True


print(json_change_flag_state(new_flag_state="abobus", telegram_username="Katya"))
# print(json_read_data2(telegram_username="Katya"))
# print(json_add_new_padawan(padawan_telegram_username="Katya", auth_padawan_pin="123",
#                          padawan_full_name="Ларионова Екатерина Сергеевна"))
# print(json_read_group_list(jedi_telegram_username="deadwacko"))
# print(json_read_padawans_list(jedi_telegram_username="deadwacko", group_name="Mini2776_С-18"))
# print(json_group_find_pin(auth_padawan_pin=123456))


# print(json_check(required_verification="group", jedi_telegram_username="deadwacko", group_name="Mini2776_С-18"))
# print(json_check(required_verification="jedi", jedi_telegram_username="deadwacko"))
# print(json_check(required_verification="padawan", jedi_telegram_username="deadwacko", group_name="Mini2776_С-18",
# padawan_telegram_username="test nickname padawan 1"))


"""with open('data.JSON', 'r', encoding="utf-8") as f:
    json_data = json.load(f)

    print(json_data["jedi"]["test_tg"]['padawan_group'].keys())"""

# print(json_add_new_jedi(jedi_kodland_email="@gmail.com", jedi_telegram_username="JEDI_TG", jedi_full_name="IVAN"))
# print(json_add_new_group(group_name="newmini123", lesson_day="1", lesson_time="12:00", number_last_lesson="м2у3",
#                         course_name="цифровое творчество", jedi_telegram_username="JEDI_TG",
#                         auth_padawan_pin="123456"))

# print(json_add_new_padawan(padawan_telegram_username="Julia", auth_padawan_pin="123",
#                           padawan_full_name="Демиденко Юлия Игоревна"))


# функция добавления нового преподавателя
# название ф-и: json_add_new_jedi()

# Входные параметры: jedi_kodland_email, jedi_telegram_username, jedi_full_name
# Выходные параметры: True/False
#                               True(Если пользователь добавлен или он уже есть)
#                               False(Если произошла ошибка)
# Вспомогательные функции:  Функция проверки наличия преподавателя в JSON файле
#  функция добавление новой группы
# название ф-и: json_add_new_group()
# Входные параметры: group_name, lesson_day, lesson_time, number_last_lesson, course_name, jedi_telegram_username,
# auth_padawan_pin
# Выходные параметры: True/False
#                               True(Если группа добавлена или она уже есть)
#                               False(Если произошла ошибка)
# Вспомогательные функции:  Функция проверки наличия группы в JSON файле json_check(group)
#  функция добавления ученика в группу
# название ф-и: json_add_new_padawan()
# Входные параметры: padawan_telegram_username, auth_padawan_pin, padawan_full_name
# Выходные параметры: True/False
#                               True(Если ученик добавлен или он уже есть)
#                               False(Если произошла ошибка)
# Вспомогательные функции:  Функция проверки наличия ученика в JSON файле json_check()
#
#  универсальная функция проверки:
# название ф-и: json_check()
# Входные параметры: jedi_kodland_email, jedi_telegram_username, jedi_full_name, group_name,
# padawan_telegram_username, required_verification
#
# Выходные параметры: True/False
#                               True(проверка нашла совпадения)
#                               False(проверка не нашла совпадений)
#                               error_name(передать название ошибки, если она возникла)
#
# Вспомогательные функции:  ---
#
# 1) Наличия преподавателя в JSON
# 2) Наличия ученика в JSON
# 3) Наличия группы в JSON
#
#  функция изменения состояния преподавателя
# название ф-и: json_change_jedi_flag_state()
# Входные параметры: new_flag_state
# Выходные параметры: True/False
#                               True(Если все ок)
#                               False(Если произошла ошибка)
#
#  функция изменения состояния ученика
# название ф-и: json_change_padawan_flag_state()
# Входные параметры: new_flag_state
# Выходные параметры: True/False
#                               True(Если все ок)
#                               False(Если произошла ошибка)
#
#  функция чтения состояния преподавателя
# название ф-и: json_read_jedi_flag_state()
# Входные параметры: нет
# Выходные параметры: True/False, current_flag_state
#                               True(Если все ок)
#                               False(Если произошла ошибка)
#
#  функция чтения состояния ученика
# название ф-и: json_read_padawan_flag_state()
# Входные параметры: нет
# Выходные параметры: True/False, current_flag_state
#                               True(Если все ок)
#                               False(Если произошла ошибка)
#
#  функция чтения всех групп определенного преподавателя
# название ф-и: json_read_group_list()
# Входные параметры: jedi_telegram_username
# Выходные параметры: True/False, current_flag_state
#                               True(Если все ок)
#                               False(Если произошла ошибка)
#
#  функция чтения учеников преподавателя определенной группы
# название ф-и: json_read_padawans_list()
# Входные параметры: jedi_telegram_username, group_name
# Выходные параметры: True/False, current_flag_state
#                               True(Если все ок)
#                               False(Если произошла ошибка)
# Изменение состояния преподавателя
"""def json_change_jedi_flag_state(new_flag_state, jedi_telegram_username):
    with open('data.JSON', 'r', encoding="utf-8") as f:
        json_data = json.load(f)
        json_data["jedi"][jedi_telegram_username]["jedi_flag_state"] = new_flag_state

    with open('data.JSON', 'w', encoding="utf-8") as f:
        f.write(json.dumps(json_data, ensure_ascii=False))
        f.close()
    return True


# Изменение состояния ученика
def json_change_padawan_flag_state(new_flag_state=None, input_padawan_telegram_username=None):
    with open('data.JSON', 'r', encoding="utf-8") as f:
        json_data = json.load(f)
        for jedi_telegram_username in json_data["jedi"].keys():

            for group_name in json_data["jedi"][jedi_telegram_username]["padawans_groups"].keys():

                for padawan in json_data["jedi"][jedi_telegram_username]["padawans_groups"][group_name][
                    "padawans"].keys():

                    if padawan == input_padawan_telegram_username:
                        json_data["jedi"][jedi_telegram_username]["padawans_groups"][group_name]["padawans"][
                            input_padawan_telegram_username]["padawan_flag_state"] = new_flag_state

                        print(jedi_telegram_username)
                        break

    with open('data.JSON', 'w', encoding="utf-8") as f:
        f.write(json.dumps(json_data, ensure_ascii=False))
        f.close()


# Чтение состояния преподавателя
def json_read_jedi_flag_state(jedi_telegram_username):
    with open('data.JSON', 'r', encoding="utf-8") as f:
        json_data = json.load(f)
        return json_data["jedi"][jedi_telegram_username]["jedi_flag_state"]


# Чтение состояния ученика
def json_read_padawan_flag_state(padawan_telegram_username):
    with open('data.JSON', 'r', encoding="utf-8") as f:
        json_data = json.load(f)
        for jedi_telegram_username in json_data["jedi"].keys():

            for group_name in json_data["jedi"][jedi_telegram_username]["padawans_groups"].keys():

                for padawan in json_data["jedi"][jedi_telegram_username]["padawans_groups"][group_name][
                    "padawans"].keys():

                    if padawan == padawan_telegram_username:
                        return json_data["jedi"][jedi_telegram_username]["padawans_groups"][group_name]["padawans"][
                            padawan_telegram_username]["padawan_flag_state"]"""