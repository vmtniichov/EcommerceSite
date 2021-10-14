from django.urls import path
from .views import HomeView,ItemDetailView,add_to_cart

app_name = 'items'

urlpatterns = [
    path('', HomeView.as_view(), name = 'home'),
    # path('<slug>/details/', ItemDetailView.as_view(), name = 'details'),
    path("<slug>/details/", ItemDetailView,name="details"),
    path('add-to-cart/<slug>/', add_to_cart, name = 'add-to-cart'),
]