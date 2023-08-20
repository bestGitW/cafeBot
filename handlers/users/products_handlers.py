from aiogram.types import InputFile, InputMediaPhoto
from aiogram import types

from loader import dp, db, bot
from keyboards import navigation_products_callback, product_count_callback
from keyboards.inlines import get_product_inline_keyboard


@dp.message_handler(text=['Список товаров'])
@dp.message_handler(commands=['products'])
async def answer_menu_command(message: types.Message):
    first_products_info = db.select_product_info(id=1)
    first_products_info = first_products_info[0]
    _, title, count, photo_path = first_products_info
    products_text = f"Название товара: {title}" \
                    f"\nКоличество товара: {count}"
    photo = InputFile(path_or_bytesio=photo_path)
    await message.answer_photo(photo=photo,
                               caption=products_text,
                               reply_markup=get_product_inline_keyboard())

@dp.callback_query_handler(navigation_products_callback.filter(for_data='products'))
async def see_new_product(call: types.CallbackQuery):
    print(call.data)
    current_product_id = int(call.data.split(':')[-1])
    first_products_info = db.select_product_info(id=current_product_id)
    first_products_info = first_products_info[0]
    _, title, count, photo_path = first_products_info
    products_text = f'Название товара: {title}' \
                    f'\nКоличество товара: {count}'

    photo = InputFile(path_or_bytesio=photo_path)
    await bot.edit_message_media(media=InputMediaPhoto(media=photo,
                                                       caption=products_text),
                                 chat_id=call.message.chat.id,
                                 message_id=call.message.message_id,
                                 reply_markup=get_product_inline_keyboard(id=current_product_id))

@dp.callback_query_handler(product_count_callback.filter(target='product_plus'))
async def plus_product(call: types.CallbackQuery):
    current_count = int(call.data.split(':')[-1])
    current_product_id = int(call.data.split(':')[-2])
    product_info = db.select_product_info(id=current_product_id)
    product_info = product_info[0]
    _, title, count, photo_path = product_info
    if current_count != count:
        current_count += 1
        products_text = f'Название товара: {title}' \
                        f'\nКоличество товара: {count}'

        photo = InputFile(path_or_bytesio=photo_path)
        await bot.edit_message_media(media=InputMediaPhoto(media=photo,
                                                           caption=products_text),
                                     chat_id=call.message.chat.id,
                                     message_id=call.message.message_id,
                                     reply_markup=get_product_inline_keyboard(id=current_product_id,
                                                                              current_count=current_count))

@dp.callback_query_handler(product_count_callback.filter(target='product_minus'))
async def minus_product(call: types.CallbackQuery):
    current_count = int(call.data.split(':')[-1])
    current_product_id = int(call.data.split(':')[-2])
    product_info = db.select_product_info(id=current_product_id)
    product_info = product_info[0]
    _, title, count, photo_path = product_info
    if current_count != 1:
        current_count -= 1
        products_text = f'Название товара: {title}' \
                        f'\nКоличество товара: {count}'

        photo = InputFile(path_or_bytesio=photo_path)
        await bot.edit_message_media(media=InputMediaPhoto(media=photo,
                                                           caption=products_text),
                                     chat_id=call.message.chat.id,
                                     message_id=call.message.message_id,
                                     reply_markup=get_product_inline_keyboard(id=current_product_id,
                                                                              current_count=current_count))

@dp.callback_query_handler(product_count_callback.filter(target='basket'))
async def add_product_basket(call: types.CallbackQuery):
    current_count = int(call.data.split(':')[-1])
    current_product_id = (call.data.split(':')[-2])
    user_id, user_basket = db.select_user_basket(id=call.from_user.id)
    # "1:23 4:80 313:2"
    # .split() -> ["1:23", "4:80", "313:2"]
    # .split(":") -> [["1", "23"], ["4", "80"], ["313", "2"], ["432", "123"]]
    user_basket = [product_data.split(':') for product_data in user_basket.split()]
    # Проверяем, есть ли уже этот товар в корзине или нет
    for i in range(len(user_basket)):
        product_id, product_count = user_basket[i]
        if current_product_id == product_id:
            user_basket[i][1] = str(int(product_count) + current_count)
            break
    else:
        user_basket += [[current_product_id, str(current_count)]]
    user_basket = ' '.join([':'.join(dbl) for dbl in user_basket])
    db.update_basket(id=user_id, user_basket=user_basket)
    await bot.answer_callback_query(callback_query_id=call.id,
                                    text='Товар успешно добавлен',
                                    show_alert=False)
