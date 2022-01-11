import json

def print_group_json():
    with open('data.JSON', 'r',encoding="utf-8") as f:
        json_data = json.load(f)
        str = ""
        for i in json_data["jedi"]["TEST_JEDI_USERNAME"]["podavans_group"].keys():
            str += i
        f.close()
        return str


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




            json_data["jedi"]["TEST_JEDI_USERNAME"]["podavans_group"][input_new_group] = x

        with open('data.JSON', 'w', encoding="utf-8") as f:
            f.write(json.dumps(json_data, ensure_ascii=False))
            f.close()
    else:
        print("Группа есть")


#функция добавления нового ученика
def add_new_podavan_json(input_group,nik_telegram,podavan_name):
    str = print_group_json()
    print(print_group_json())
    print(input_group)
    if input_group  in str:
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

            json_data["jedi"]["Костюкевич Михаил Константинович"]["podavans_group"][input_group]["podavans"][nik_telegram] = x

        with open('data.JSON', 'w', encoding="utf-8") as f:
            f.write(json.dumps(json_data, ensure_ascii=False))
            f.close()
    else:
        print("Такой группы нет")



#функция добавления нового преподавателя
def json_add_new_jedi(jedi_kodland_email=None, jedi_telegram_username=None, jedi_full_name=None):
    with open('data.JSON', 'r', encoding="utf-8") as f:
        json_data = json.load(f)

        add_pattern_jedi = {
            "full_name": f"{jedi_full_name}",
            "jedi_kodland_email": f"{jedi_kodland_email}",
            "podavan_group":{}
        }

        json_data["jedi"][jedi_telegram_username] = add_pattern_jedi


    with open('data.JSON', 'w', encoding="utf-8") as f:
        f.write(json.dumps(json_data, ensure_ascii=False))
        f.close()


#функция проверки
def json_check(required_verification, jedi_kodland_email=None, jedi_telegram_username=None, jedi_full_name=None,
               group_name=None,padawan_telegram_username=None):

    #проверка на группу
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

    #проверка на преподавателя (по нику телеграма)
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
    #проверка ученика (по нику телеграма)
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






print(json_check(required_verification="group", jedi_telegram_username="deadwacko", group_name="Mini2776_С-18"))
print(json_check(required_verification="jedi", jedi_telegram_username="deadwacko"))
print(json_check(required_verification="padawan", jedi_telegram_username="deadwacko", group_name="Mini2776_С-18", padawan_telegram_username="test nickname padawan 1"))



"""with open('data.JSON', 'r', encoding="utf-8") as f:
    json_data = json.load(f)

    print(json_data["jedi"]["test_tg"]['padawan_group'].keys())"""




###json_add_new_jedi(jedi_kodland_email="@gmail.com", jedi_telegram_username="JEDI_TG", jedi_full_name="IVAN")







#TODO функция добавления нового преподавателя
#     название ф-и: json_add_new_jedi()
#     Входные параметры: jedi_kodland_email, jedi_telegram_username, jedi_full_name
#     Выходные параметры: True/False
#                                   True(если пользователь добавлен или он уже есть)
#                                   False(Если произошла ошибка)
#     Вспомогательные функции:  Функция проверки наличия преподавателя в JSON файле



#TODO функция добавление новой группы

#TODO функция добавления ученика в группу









#TODO универсальная функция проверки:
#     название ф-и: json_check()
#     Входные параметры: jedi_kodland_email, jedi_telegram_username, jedi_full_name, group_name,
#     padawan_telegram_username, required_verification
#
#     Выходные параметры: True/False
#                                   True(проверка нашла совпадения)
#                                   False(проверка не нашла совпадений)
#                                   error_name(передать название ошибки, если она возникла)
#
#     Вспомогательные функции:  ---
#
#     1) Наличия преподавателя в JSON
#     2) Наличия ученика в JSON
#     3) Наличия группы в JSON






#TODO
