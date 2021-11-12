from django.urls import path
from .views import HomeView,CartView,OrderListView,OrderDetailView,item_search_view,filter_by_category,ItemDetailView,add_to_cart,remove_from_cart,OrderProcessDone,OrderFilter

app_name = 'items'

urlpatterns = [
    path('', HomeView.as_view(), name = 'home'),
    # path('<slug>/details/', ItemDetailView.as_view(), name = 'details'),
    path("details/<slug>/", ItemDetailView,name="details"),
    path('add-to-cart/<slug>/', add_to_cart, name = 'add-to-cart'),
    path('cart/', CartView.as_view(), name = 'cart'),
    path('search/', item_search_view, name = 'search'),
    path('filter/<pk>', filter_by_category, name = 'filter-by-cate'),
    path('remove-from-cart/<slug>/<size>', remove_from_cart, name = 'remove-from-cart'),
    path('orders/', OrderListView.as_view(), name = 'orders'),
    path('order/<pk>', OrderDetailView.as_view(), name = 'order-details'),
    path('orders/<state>', OrderFilter, name = 'order-filter'),
    path('order-process-done/<pk>', OrderProcessDone, name = 'order-process-done'),
]