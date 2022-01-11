from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


#start keyboard
jedi_button = InlineKeyboardButton('Преподаватель', callback_data='event_jedi_button')
padawan_button = InlineKeyboardButton('Ученик', callback_data='event_padawan_button')
start_keyboard_markup = InlineKeyboardMarkup().add(jedi_button).add(padawan_button)

#refund keyboard(jedi)
refund_button = InlineKeyboardButton('Вернуться к началу', callback_data='event_refund_button')
refund_keyboard_markup = InlineKeyboardMarkup().add(refund_button)

#jedi menu keyboard(jedi)
add_group_button = InlineKeyboardButton('Добавить группу', callback_data='event_add_group_button')
show_stats_button = InlineKeyboardButton('Посмотреть статистику', callback_data='event_show_stats_button')
mailing_button = InlineKeyboardButton('Отправить рассылку', callback_data='event_mailing_button')
jedi_menu_keyboard_markup = InlineKeyboardMarkup().add(add_group_button).add(show_stats_button).add(mailing_button)

#stat keyboard(jedi)
student_rate_button = InlineKeyboardButton('Рейтинг от учеников', callback_data='event_student_rate_button')
show_groups_button = InlineKeyboardButton('Посмотреть группы', callback_data='event_student_rate_button')
statistic_keyboard_markup = InlineKeyboardMarkup().add(student_rate_button).add(show_groups_button)

#visitation keyboard(padawan)
visit_button = InlineKeyboardButton('Буду на уроке!', callback_data='event_visit_button')
truancy_button = InlineKeyboardButton('Не смогу присутствовать на уроке', callback_data='event_truancy_button')
visitation_keyboard_markup = InlineKeyboardMarkup().add(visit_button).add(truancy_button)









