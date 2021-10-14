from django.shortcuts import render, get_object_or_404,redirect
from django.http import request
from django.urls.base import reverse
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import OrderItemForm
from .models import Item, Order,OrderItem
from django.contrib import messages

# Create your views here.

class HomeView(ListView):
    paginate_by = 10
    template_name = 'index.html'
    model = Item
    context_object_name = 'items'

def ItemDetailView(request, slug):
    if request.method == "GET":
        item = Item.objects.filter(slug=slug)[0]
        form = OrderItemForm()
        context = {
            "item":item,
            "form":form
        }
        return render(request, "items/item_details.html", context=context)
    
    elif request.method == "POST":

        if "size" in request.POST:
            return add_to_cart(request, slug)
        else:
            msg = f"Please select item's size!"
            messages.error(request,msg)
            return redirect("items:details", slug=slug)
        

        

@login_required
def add_to_cart(request, slug):

    size = request.POST['size']
    order_qs = Order.objects.filter(user = request.user,order_state = False)
    item = get_object_or_404(Item, slug = slug)
    if order_qs.exists():
        order = order_qs[0]#Lấy order đầu tiên nếu order_qs có giá trị

        # Tìm item tương ứng để lấy nếu k sẽ tạo OrderItem mới tương ứng
        order_item,_ = OrderItem.objects.get_or_create(Item, order=order)

        if order.items.filter(item__slug = item.slug):
            # Nếu đã có Item 
            order_item.quantity +=1
            order_item.save()
            msg = f"Added {item.name}({size})to  your cart!"
            return redirect("items:details", slug=slug)

    msg = f"Added {item.name}({size}) to your cart!"
    messages.info(request,msg)
    return redirect("items:details", slug=slug)
        