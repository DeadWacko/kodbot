from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


#Стартовая клавиатура
jedi_button = InlineKeyboardButton('Джедай!', callback_data='event_jedi_button')
padawan_button = InlineKeyboardButton('Падаван', callback_data='event_padawan_button')
start_keyboard_markup = InlineKeyboardMarkup().add(jedi_button).add(padawan_button)

#Клавиатура возврата в начальное меню (ветка преподавателя)
refund_button = InlineKeyboardButton('Вернуться к началу', callback_data='event_refund_button')
refund_keyboard_markup = InlineKeyboardMarkup().add(refund_button)

#Клавиатура возможностей (ветка преподавателя)
add_group_button = InlineKeyboardButton('Добавить группу', callback_data='event_add_group_button')
show_stats_button = InlineKeyboardButton('Посмотреть статистику', callback_data='event_show_stats_button')
mailing_button = InlineKeyboardButton('Отправить рассылку', callback_data='event_mailing_button')
jedi_menu_keyboard_markup = InlineKeyboardMarkup().add(add_group_button).add(show_stats_button).add(mailing_button)

#Клавиатура статистики (ветка преподавателя)
student_rate_button = InlineKeyboardButton('Рейтинг от учеников', callback_data='event_student_rate_button')
show_groups_button = InlineKeyboardButton('Посмотреть группы', callback_data='event_student_rate_button')











