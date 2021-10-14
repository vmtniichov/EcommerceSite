from django import forms
from django.forms import widgets

from items.models import Item

sizes = (
    ('S', 'S'),
    ('M', 'M'),
    ('L', 'L'),
    ('XL', 'XL')
)
class OrderItemForm(forms.Form):
    item_size = forms.ChoiceField(choices=sizes, widget=forms.RadioSelect(attrs={'require':True}))
    

    