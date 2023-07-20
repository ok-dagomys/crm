# @dp.message_handler(commands=['start'])
# async def send_welcome(message: types.Message):
#     kb = [
#         [
#             types.KeyboardButton(text="Сможешь это повторить?"),
#             types.KeyboardButton(text="А это?")
#         ],
#     ]
#     keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, keyboard=kb)
#     await message.reply("Привет!\nЯ Эхобот!\nОтправь мне любое сообщение.", reply_markup=keyboard)
#
#
# urlkb = InlineKeyboardMarkup(row_widht=1)
# urlButton_1 = InlineKeyboardButton(text='Habr', url='https://www.habr.com', callback_data='btn1')
# urlButton_2 = InlineKeyboardButton(text='VC', callback_data='btn2')
# urlkb.add(urlButton_1, urlButton_2)
#
#
# @dp.message_handler(commands='url')
# async def url_command(message: types.Message):
#     await message.answer('It-news:', reply_markup=urlkb)
#
#
# @dp.callback_query_handler(lambda c: c.data and c.data.startswith('btn'))
# async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
#     code = callback_query.data[-1]
#     if code.isdigit():
#         code = int(code)
#     if code == 1:
#         await bot.answer_callback_query(callback_query.id, text='Новостной портал Хабр')
#     elif code == 2:
#         await bot.answer_callback_query(callback_query.id, text='Новостной портал VC', show_alert=True)
#     else:
#         await bot.answer_callback_query(callback_query.id)



