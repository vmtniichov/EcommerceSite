from django.shortcuts import render, get_object_or_404,redirect
from django.http import request
from django.urls.base import reverse
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from .forms import OrderItemForm
from .models import Item, Order,OrderItem
from django.contrib import messages

class HomeView(ListView):
    paginate_by = 10
    template_name = 'index.html'
    model = Item
    context_object_name = 'items'

class CartView(LoginRequiredMixin,View):

    def get(self, *args, **kwargs):
        order_qs = Order.objects.filter(user = self.request.user, order_state = False)
        if order_qs.exists():
            order = order_qs[0]
            context = {'order': order}
            return render(self.request, "items/cart.html",context)
        else:
            messages.warning(self.request, "Nothing in your cart!")
            return render(self.request, 'items/cart.html', )


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
        order_item,_ = OrderItem.objects.get_or_create(item=item, order=order, size=size)

        if order.items.filter(item__slug = item.slug,size=size):
            # Nếu đã có Item 
            order_item.quantity +=1
            order_item.save()
            order.save()
            msg = f"Added {item.name}({size})to  your cart!"
            messages.info(request,msg)
            return redirect("items:details", slug=slug)
        else:
            order.items.add(order_item)
            order.save()
            msg = f"Added {item.name}({size})to  your cart!"
            messages.info(request,msg)
            return redirect("items:details", slug=slug)
    else:
        order = Order.objects.create(user=request.user)
        order_item = OrderItem.objects.create(item = item,size=size)
        order.items.add(order_item)
        msg = f"Added {item.name}({size})to  your cart!"
        messages.info(request,msg)
        return redirect("items:details", slug=slug)
        

@login_required
def remove_from_cart(request,slug,size):

    item = get_object_or_404(Item, slug = slug)
    order_qs = Order.objects.filter(user = request.user, order_state = False)
    
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug = item.slug):
            #lấy danh sách order_item của order có trạng thái là false
            order_item_qs = OrderItem.objects.filter(item = item, order=order,size=size)
            
            if order_item_qs.exists():
                order_item = order_item_qs[0]
                msg = f'Deleted {order_item.item.name}({order_item.size}) from cart.'
                order.items.remove(order_item)
                order_item.delete()
                messages.warning(request,msg)
                return redirect("items:cart")
            else:
                messages.warning(request,'Item not in your cart.')
                return redirect("items:cart")



        