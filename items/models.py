from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth import get_user_model

from accounts.models import Address
# Create your models here.

User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

    class Meta():
        verbose_name_plural = 'Categories'
    

class Item(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(blank=True)
    price = models.PositiveIntegerField(default=0)
    discount_price = models.IntegerField(blank=True, null=True)
    categories = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to = 'static/media/item-images',blank=True,null = True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Item, self).save(*args,**kwargs)

    def item_formated_price(self):
        return f"{self.price:,} VND"

    def item_formated_discount_price(self):
        return f"{self.discount_price:,} VND"

    def get_final_item_formated_price(self):
        return self.item_formated_discount_price() if self.discount_price else self.item_formated_price()

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        ordering = ['id']

class OrderItem(models.Model):
    item = models.ForeignKey("Item", on_delete=models.CASCADE)
    size = models.CharField(max_length=3, null = True, blank=True)
    quantity = models.PositiveIntegerField(default=1)

    def get_final_price(self):
        return self.item.discount_price if self.item.discount_price else self.item.price

    def get_item_total(self):
        total = self.get_final_price() * self.quantity
        return total
    def get_item_total_formated(self):
        return f"{self.get_item_total():,} VND"

    def __str__(self) -> str:
        return f"{self.item.name}({self.size})"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField("OrderItem")
    create_date = models.DateTimeField(auto_now=timezone.now)
    order_date = models.DateTimeField(blank=True,null=True)
    order_state = models.BooleanField(default = False)
    order_total = models.PositiveIntegerField(default=0, blank=True, null=True)

    shipping_address = models.ForeignKey(Address, blank=True,null=True, on_delete=models.CASCADE)
    process = models.BooleanField(default=False,blank=True,null=True)
    payment_method = models.CharField(max_length=64, blank=True,null=True)


    def get_order_total(self):
        total = 0
        for order_item in self.items.all():
            total+=order_item.get_item_total()
        return f"{total:,} VND"

    def set_order_total(self):
        total = 0
        for order_item in self.items.all():
            total+=order_item.get_item_total()
        self.order_total = total
        self.save()

    def __str__(self) -> str:
        return f"Order No.{self.pk}--Username:{self.user.username}"



