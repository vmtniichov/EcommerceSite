from django.shortcuts import render, get_object_or_404,redirect
from django.urls.base import reverse
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
# from django.http import JsonResponse
from django.views.generic.base import TemplateView

from .forms import OrderItemForm
from .models import Item, Order,OrderItem,Category

class HomeView(ListView):
    paginate_by = 10
    template_name = 'index.html'
    model = Item
    context_object_name = 'items'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        context.update({
            "categories":categories
        })
        return context
# class HomeView(TemplateView):
#     template_name = 'index.html'
# class ItemJsonListView(View):
#     def get(self,*args,**kwargs):
#         upper = kwargs.get("num_items")
#         lower = upper - 5
#         items = list(Item.objects.values()[lower:upper])
#         items_size = len(Item.objects.all())
#         max_size = True if upper >= items_size else False
#         return JsonResponse({'items':items,'max_size':max_size},safe=False)

class CartView(LoginRequiredMixin,View):

    def get(self, *args, **kwargs):
        order_qs = Order.objects.filter(user = self.request.user, order_state = False)
        if order_qs.exists():
            order = order_qs[0]
            context = {'order': order}
            return render(self.request, "items/cart.html",context)
        else:
            return render(self.request, 'items/cart.html', )

def item_search_view(request):
    if request.method == "POST":
        print(request.POST)
        search = request.POST['searchBar']
        items = Item.objects.filter(name__icontains = search)
        context = {
            'items':items
        }
        return render(request, 'items/item_search.html', context)
    elif request.method =="GET":
        return redirect("items:filter-by-cate")

def filter_by_category(request,pk):
    items = Item.objects.filter(categories_id = pk)
    context = {
            'items':items
        }
    return render(request, 'items/item_search.html', context)

class OrderListView(LoginRequiredMixin, View):

    def get(self, *args, **kwargs):
        if(self.request.user.is_superuser):
            order_qs = Order.objects.filter(order_state=True).order_by("-order_date")
            context = {"orders": order_qs}
            return render(self.request, "orders/order_list.html", context)
        else:
            order_qs = Order.objects.filter(user = self.request.user,order_state=True).order_by("-order_date")
            context = {"orders": order_qs}
            return render(self.request, "orders/order_list.html", context)

@login_required
def OrderFilter(request,state=None):
    if(request.user.is_superuser):
        order_qs = Order.objects.filter(order_state=True, process=state).order_by("-order_date")
        context = {"orders":order_qs}
        return render(request,"orders/order_list.html",context)
    else:
        order_qs = Order.objects.filter(user=request.user, order_state=True, process=state).order_by("-order_date")
        context = {"orders":order_qs}
        return render(request,"orders/order_list.html",context)

class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    context_object_name = "order"
    template_name = 'orders/order_details.html'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Order.objects.all()
        else:
            user = self.request.user
            return user.order_set.all()

#cập nhật trạng thái đơn hàng
@login_required
def OrderProcessDone(request,pk):
    if request.user.is_superuser:
        order_qs = Order.objects.filter(pk=pk, order_state=True)
        if order_qs.exists():
            order = order_qs[0]
            order.process = True
            order.save()
            return redirect("items:orders")
        return redirect("items:orders")
    else:
        return redirect("items:orders")

def cancel_order(request,pk):
    if request.user.is_superuser:
        order_qs = Order.objects.filter(pk=pk, order_state=True)
        if order_qs.exists():
            order = order_qs[0]
            order.process = False
            order.save()
            return redirect("items:orders")
        return redirect("items:orders")

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
            msg = f"Vui lòng chọn kích thước sản phẩm!"
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
            # order.save()
            order.set_order_total()
            msg = f"Đã thêm {item.name}({size}) vào giỏ hàng!"
            messages.info(request,msg)
            return redirect("items:details", slug=slug)
        else:
            order.items.add(order_item)
            # order.save()
            order.set_order_total()

            msg = f"Đã thêm {item.name}({size}) vào giỏ hàng!"
            messages.info(request,msg)
            return redirect("items:details", slug=slug)
    else:
        order_item = OrderItem.objects.create(item = item,size=size)
        order = Order.objects.create(user=request.user)
        order.items.add(order_item)
        order.set_order_total()
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
            
            #lấy danh sách order_item theo item, order, size
            order_item_qs = OrderItem.objects.filter(item = item, order=order,size=size)
            
            if order_item_qs.exists():
                order_item = order_item_qs[0]
                msg = f'Đã xóa {order_item.item.name}({order_item.size}) khỏi giỏ hàng.'
                order.items.remove(order_item)
                order_item.delete()
                messages.warning(request,msg)
                return redirect("items:cart")
            else:
                messages.warning(request,'Item not in your cart.')
                return redirect("items:cart")

@login_required
def remove_single_item_from_cart(request,slug,size):
    item = get_object_or_404(Item, slug = slug) 
    order_qs = Order.objects.filter(user = request.user, order_state = False)
    

    if order_qs.exists():
        order = order_qs[0]
        order_item, _ = OrderItem.objects.get_or_create(item = item, order=order,size=size)

        if order.items.filter(item__slug = item.slug):
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
                return redirect("items:cart")
            else:
                order_item.delete()
                return redirect("items:cart")

@login_required
def increase_quantity(request,slug,size):
    item = get_object_or_404(Item, slug = slug) 
    order_qs = Order.objects.filter(user = request.user, order_state = False)
    if order_qs.exists():
        order = order_qs[0]
        order_item, _ = OrderItem.objects.get_or_create(item = item, order=order,size=size)
        order_item.quantity += 1
        order_item.save()
        return redirect("items:cart")
    else:
        return redirect("items:cart")

    