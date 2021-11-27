from django.urls import path
from .views import UserCreateView, UserDetailView, UserUpdateView,PwdChangeView, CreateAddressView, UpdateAddressView,CheckoutView ,remove_address, load_district, load_ward

app_name = "accounts"

urlpatterns = [
    path('dang-ky/', UserCreateView.as_view(), name = "signup"),
    path('thong-tin-ca-nhan/', UserDetailView.as_view(), name = "profile"),
    path('cap-nhat-thong-tin/', UserUpdateView.as_view(), name = "update"),
    path('thay-doi-mat-khau/', PwdChangeView.as_view(), name = "pwd-change"),
    path('them-dia-chi/', CreateAddressView.as_view(), name = "new-address"),
    path('cap-nhat-dia-chi/<pk>', UpdateAddressView.as_view(), name = "update-address"),
    path('remove-address/<pk>', remove_address, name = "remove-address"),
    path('ajax/load-districts/', load_district, name = "ajax-load-districts"),
    path('ajax/load-wards/', load_ward, name = "ajax-load-wards"),
    path('thanh-toan/', CheckoutView.as_view(), name = "checkout"),
]