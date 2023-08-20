from aiogram.utils.callback_data import CallbackData

navigation_products_callback = CallbackData('navigation_products_btm', 'for_data', 'id')
product_count_callback = CallbackData('product_count_btm', 'target', 'id', 'current_count')
basket_callback = CallbackData('change_btm', 'action')