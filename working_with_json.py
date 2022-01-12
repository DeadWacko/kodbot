import json


# функция добавления нового преподавателя
def json_add_new_jedi(jedi_kodland_email=None, jedi_telegram_username=None, jedi_full_name=None):
    if not json_check(required_verification="jedi", jedi_telegram_username=jedi_telegram_username):
        with open('data.JSON', 'r', encoding="utf-8") as f:
            json_data = json.load(f)

            add_pattern_jedi = {
                "jedi_flag_state": "",
                "full_name": f"{jedi_full_name}",
                "jedi_kodland_email": f"{jedi_kodland_email}",
                "podawans_groups": {}
            }

            json_data["jedi"][jedi_telegram_username] = add_pattern_jedi

        with open('data.JSON', 'w', encoding="utf-8") as f:
            f.write(json.dumps(json_data, ensure_ascii=False))
            f.close()
        return True
    else:
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
    if input_group_name[0]:
        print("Группа по пину найдена")
        print(input_group_name[2])
        if not json_check(required_verification="padawan", padawan_telegram_username=padawan_telegram_username,
                          jedi_telegram_username=input_group_name[2], group_name=input_group_name[1]):
            print("Ученик потерялса")

            with open('data.JSON', 'r', encoding="utf-8") as f:
                json_data = json.load(f)

                add_pattern_padawan = {
                    "padawan_flag_state": "",
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
                print(1111111111111111111111111111111111111111111111111111)
                json_data["jedi"][input_group_name[2]]["padawans_groups"][input_group_name[1]]["padawans"][
                    padawan_telegram_username] = add_pattern_padawan

            with open('data.JSON', 'w', encoding="utf-8") as f:
                f.write(json.dumps(json_data, ensure_ascii=False))
                f.close()
            return True
        else:
            return True
    else:
        return False


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


# Изменение состояния преподавателя
def json_change_jedi_flag_state(new_flag_state, jedi_telegram_username):
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
                            padawan_telegram_username]["padawan_flag_state"]