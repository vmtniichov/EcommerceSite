from django.urls import path
from .views import HomeView,CartView,OrderListView,OrderDetailView,item_search_view,filter_by_category,ItemDetailView,add_to_cart,remove_from_cart,OrderProcessDone,OrderFilter

app_name = 'items'

urlpatterns = [
    path('', HomeView.as_view(), name = 'home'),
    # path('items-json/<int:num_items>/',ItemJsonListView.as_view(),name="items-json"),
    path("chi-tiet-san-pham/<slug>/", ItemDetailView,name="details"),
    path('add-to-cart/<slug>/', add_to_cart, name = 'add-to-cart'),
    path('gio-hang/', CartView.as_view(), name = 'cart'),
    path('tim-kiem/', item_search_view, name = 'search'),
    path('danh-muc/<pk>', filter_by_category, name = 'filter-by-cate'),
    path('remove-from-cart/<slug>/<size>', remove_from_cart, name = 'remove-from-cart'),
    path('don-hang/', OrderListView.as_view(), name = 'orders'),
    path('chi-tiet-don-hang/<pk>', OrderDetailView.as_view(), name = 'order-details'),
    path('don-hang/<state>', OrderFilter, name = 'order-filter'),
    path('order-process-done/<pk>', OrderProcessDone, name = 'order-process-done'),
]