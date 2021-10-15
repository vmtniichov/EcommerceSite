from django.urls import path
from .views import HomeView,CartView,ItemDetailView,add_to_cart,remove_from_cart

app_name = 'items'

urlpatterns = [
    path('', HomeView.as_view(), name = 'home'),
    # path('<slug>/details/', ItemDetailView.as_view(), name = 'details'),
    path("<slug>/details/", ItemDetailView,name="details"),
    path('add-to-cart/<slug>/', add_to_cart, name = 'add-to-cart'),
    path('cart/', CartView.as_view(), name = 'cart'),
    path('remove-from-cart/<slug>/<size>', remove_from_cart, name = 'remove-from-cart'),
]