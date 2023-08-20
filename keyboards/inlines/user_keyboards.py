from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inlines.callback_data import navigation_products_callback, basket_callback, \
    product_count_callback
from loader import db

def get_product_inline_keyboard(id: int = 1, current_count: int = 1) -> InlineKeyboardMarkup:
    product_inline_keyoard = InlineKeyboardMarkup()
    left_id = id - 1
    right_id = id + 1
    if id == 1:
        btm = InlineKeyboardButton(text='>>>',
                                   callback_data=navigation_products_callback.new(
                                       for_data='products',
                                       id=right_id)
                                   )
        product_inline_keyoard.add(btm)
    elif id == db.get_product_count():
        btm = InlineKeyboardButton(text='<<<',
                                   callback_data=navigation_products_callback.new(
                                       for_data='products',
                                       id=left_id)
                                   )
        product_inline_keyoard.add(btm)
    else:
        btm_left = InlineKeyboardButton(text='<<<',
                                        callback_data=navigation_products_callback.new(
                                            for_data='products',
                                            id=left_id)
                                       )
        btm_right = InlineKeyboardButton(text='>>>',
                                         callback_data=navigation_products_callback.new(
                                            for_data='products',
                                            id=right_id)
                                        )
        product_inline_keyoard.row(btm_left, btm_right)
    product_inline_keyoard.row(InlineKeyboardButton(text='-',
                                                    callback_data=product_count_callback.new(
                                                        target='product_minus',
                                                        id=id,
                                                        current_count=f'{current_count}'
                                                    )),
                               InlineKeyboardButton(text=f'{current_count}',
                                                    callback_data=product_count_callback.new(
                                                        target='None',
                                                        id=id,
                                                        current_count=f'{current_count}'
                                                    )),
                               InlineKeyboardButton(text='+',
                                                    callback_data=product_count_callback.new(
                                                        target='product_plus',
                                                        id=id,
                                                        current_count=f'{current_count}'
                                                    )),
                               )
    product_inline_keyoard.row(InlineKeyboardButton(text='В корзину',
                                                    callback_data=product_count_callback.new(
                                                        target='basket',
                                                        id=id,
                                                        current_count=f'{current_count}')
                                                    ))
    return product_inline_keyoard

basket_keyboards = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Очистить',
                                 callback_data=basket_callback.new(
                                     action='del_basket'
                                 ))
        ],
        [
            InlineKeyboardButton(text='Оформить заказ',
                                 callback_data=basket_callback.new(
                                     action='buy'
                                 ))
        ]
    ])