from django.urls import path
from .views import *

urlpatterns = [
    path('', store,name="store"),
    path('checkout/', checkout,name="checkout"),
    path('cart/', cart,name="cart"),
    path('login/', login,name="login"),
    path('signup/', register,name="signup"),
    path('logout/', log_out,name="logout"),
    path('itemAdd/', updateItem,name="itemAdd"),
    path('process_order/', processOrder,name="process_order"),
]
