from django.urls import path
from .views import *

urlpatterns = [
    path('', show_cart, name='showcart'),
    path('add', add_to_cart, name='add_to_cart'),
    path('delete/<int:pk>', delete_from_cart, name='delete_from_cart'),
    path('handelrequest', handelrequest, name='handelrequest'),
    path('pay/<int:pk>', pay, name='pay'),
    path('orders', orders, name='orders'),
    path('track/<str:id>', track_order, name='track'),
    path('received/<str:id>', order_received, name='order_received'),
]
