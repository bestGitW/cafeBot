from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


commands_default_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Список товаров'),
        ],
        [
            KeyboardButton(text='Помощь',
                           request_location=True),
            #KeyboardButton(text='О нас')
        ],
        [
            KeyboardButton(text='Активация аккаунта',
                           request_contact=True)
        ],
        [
            KeyboardButton(text='Скрыть меню')
        ]
    ],
    resize_keyboard=True
)


# commands_default_keyboard = ReplyKeyboardMarkup(
#     keyboard=[
#         [
#             KeyboardButton(text='/start'),
#             KeyboardButton(text='/help')
#         ],
#         [
#             KeyboardButton(text='/info'),
#         ],
#         [
#             KeyboardButton(text='Подтвердите номер телефона',
#                            request_contact=True)
#         ]
#     ],
#     resize_keyboard=True
# )
#
# commands_markup_request = ReplyKeyboardMarkup(resize_keyboard=True).add(
#     KeyboardButton('Отправить свой контакт', request_contact=True)
# ).add(
#     KeyboardButton('Отправить свою локацию', request_location=True)
# )


