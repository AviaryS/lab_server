from django.urls import path
from main.views import *


urlpatterns = [
    path('login', user_login_view),
    path('signup', user_signup_view),
    path('logout', user_logout_view),

    path('product', create_product_for_admin),
    path('product/<int:product_id>', edit_or_delete_product_for_admin),
    path('products', product_list_view),

    path('cart', cart_list),
    path('cart/<int:product_id>', add_product_to_cart_or_delete),

    path('order', get_post_order_view)
]
