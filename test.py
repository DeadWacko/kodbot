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

















json_add_new_jedi(jedi_kodland_email="@gmail.com", jedi_telegram_username="JEDI_TG", jedi_full_name="IVAN")







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
#     1) Наличия преподавателя в JSON
#     2) Наличия ученика в JSON
#     3) Наличия группы в JSON






#TODO
