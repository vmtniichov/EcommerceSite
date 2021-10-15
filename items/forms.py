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
    # quantity = forms.DecimalField(min_value=1, max_value=100, max_digits=4,widget=forms.NumberInput(attrs={'class': 'text-black',
    #                                                                 }),)
    

    