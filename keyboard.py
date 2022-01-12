from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


#start keyboard
jedi_button = InlineKeyboardButton('Преподаватель 🥸', callback_data='event_jedi_button')
padawan_button = InlineKeyboardButton('Ученик 🤓', callback_data='event_padawan_button')
start_keyboard_markup = InlineKeyboardMarkup().add(jedi_button).add(padawan_button)

#refund keyboard(jedi)
refund_button = InlineKeyboardButton('Вернуться к началу ⬅️', callback_data='event_refund_button')
refund_keyboard_markup = InlineKeyboardMarkup().add(refund_button)

#jedi menu keyboard(jedi)
add_group_button = InlineKeyboardButton('Добавить группу ➕', callback_data='event_add_group_button')
show_stats_button = InlineKeyboardButton('Посмотреть статистику 📄 ', callback_data='event_show_stats_button')
mailing_button = InlineKeyboardButton('Отправить рассылку 📬 ', callback_data='event_mailing_button')
jedi_menu_keyboard_markup = InlineKeyboardMarkup().add(add_group_button).add(show_stats_button).add(mailing_button)

#stat keyboard(jedi)
show_salary_button = InlineKeyboardButton('Посмотреть зарплату 💸', callback_data='event_show_salary_button')
show_groups_button = InlineKeyboardButton('Посмотреть группы 👯‍♂️', callback_data='event_show_groups_button')
show_hours_worked_button = InlineKeyboardButton('Количество отработанных часов 🕒 ',
                                                callback_data='event_show_hours_worked_button')
show_padawans_rate_button = InlineKeyboardButton('Рейтинг учеников 📈', callback_data='event_show_padawans_rate_button')
show_jedi_rate_button =InlineKeyboardButton('Рейтинг преподавателя 📉', callback_data='event_show_jedi_rate_button')
statistic_keyboard_markup = InlineKeyboardMarkup().add(show_salary_button).add(show_groups_button)\
    .add(show_hours_worked_button).add(show_padawans_rate_button).add(show_jedi_rate_button)

#visitation keyboard(padawan)
visit_button = InlineKeyboardButton('Буду на уроке! :like: ', callback_data='event_visit_button')
truancy_button = InlineKeyboardButton('Не смогу присутствовать на уроке 👎', callback_data='event_truancy_button')
visitation_keyboard_markup = InlineKeyboardMarkup().add(visit_button).add(truancy_button)

#rate lesson button(padawan)
rate_lesson_one_button = InlineKeyboardButton('1 - очень плохо 🥺', callback_data='event_rate_lesson_one_button')
rate_lesson_two_button = InlineKeyboardButton('2', callback_data='event_rate_lesson_two_button')
rate_lesson_three_button = InlineKeyboardButton('3', callback_data='event_rate_lesson_three_button')
rate_lesson_four_button = InlineKeyboardButton('4', callback_data='event_rate_lesson_four_button')
rate_lesson_five_button = InlineKeyboardButton('5 - великолепно 🤠', callback_data='event_rate_lesson_five_button')
rate_lesson_keyboard_markup = InlineKeyboardMarkup().add(rate_lesson_one_button).add(rate_lesson_two_button)\
    .add(rate_lesson_three_button).add(rate_lesson_four_button).add(rate_lesson_five_button)

#rate work on lesson(padawan)
rate_work_one_button = InlineKeyboardButton('1 - я не справился 🥺', callback_data='event_rate_work_one_button')
rate_work_two_button = InlineKeyboardButton('2', callback_data='event_rate_work_two_button')
rate_work_three_button = InlineKeyboardButton('3', callback_data='event_rate_work_three_button')
rate_work_four_button = InlineKeyboardButton('4', callback_data='event_rate_work_four_button')
rate_work_five_button = InlineKeyboardButton('5 - все круто 🤠', callback_data='event_rate_work_five_button')
rate_work_keyboard_markup = InlineKeyboardMarkup().add(rate_work_one_button).add(rate_work_two_button)\
    .add(rate_work_three_button).add(rate_work_four_button).add(rate_work_five_button)

#rate explanations(padawan)
rate_explanations_one_button = InlineKeyboardButton('1 - ничего не понял 🥺',
                                                    callback_data='event_rate_explanations_one_button')
rate_explanations_two_button = InlineKeyboardButton('2', callback_data='event_rate_explanations_two_button')
rate_explanations_three_button = InlineKeyboardButton('3', callback_data='event_rate_explanations_three_button')
rate_explanations_four_button = InlineKeyboardButton('4', callback_data='event_rate_explanations_four_button')
rate_explanations_five_button = InlineKeyboardButton('5 - все понял 🤠', callback_data='event_rate_explanations_five_button')
rate_explanations_keyboard_markup = InlineKeyboardMarkup().add(rate_explanations_one_button).add(rate_explanations_two_button)\
    .add(rate_explanations_three_button).add(rate_explanations_four_button).add(rate_explanations_five_button)

#rate skill button(padawan)
rate_skill_one_button = InlineKeyboardButton('1 - ничего не могу 🥺', callback_data='event_rate_skill_one_button')
rate_skill_two_button = InlineKeyboardButton('2', callback_data='event_rate_skill_two_button')
rate_skill_three_button = InlineKeyboardButton('3', callback_data='event_rate_skill_three_button')
rate_skill_four_button = InlineKeyboardButton('4', callback_data='event_rate_skill_four_button')
rate_skill_five_button = InlineKeyboardButton('5 - все могу 🤠', callback_data='event_rate_skill_five_button')
rate_skill_keyboard_markup = InlineKeyboardMarkup().add(rate_skill_one_button).add(rate_skill_two_button)\
    .add(rate_skill_three_button).add(rate_skill_four_button).add(rate_skill_five_button)

#problems button(padawan)
problems_button = InlineKeyboardButton('Есть проблемы 😥', callback_data='problems_button')
no_problems_button = InlineKeyboardButton('Нет проблем 👌', callback_data='no_problems_button')
problems_keyboard_markup = InlineKeyboardMarkup().add(problems_button).add(no_problems_button)

