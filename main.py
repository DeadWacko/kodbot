from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from config import TOKEN


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)



# keyboards.py
inline_btn_1 = InlineKeyboardButton('Джедай!', callback_data='button1')
inline_btn_2 = InlineKeyboardButton('Падаван', callback_data='button2')
inline_kb1 = InlineKeyboardMarkup().add(inline_btn_1).add(inline_btn_2)

#bot.py
@dp.message_handler(commands=['start'])
async def process_command_1(message: types.Message):
    await message.reply("Привет, выбери свой статус :3", reply_markup=inline_kb1)



if __name__ == '__main__':
    executor.start_polling(dp)

