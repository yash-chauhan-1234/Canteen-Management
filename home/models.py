from email.policy import default
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Menu(models.Model):
    name=models.CharField(max_length=50)
    price=models.IntegerField()
    prep_time=models.IntegerField()
    cuisines=(
        ('0', "None"),
        ("Indian", "Indian"),
        ("Chinese", "Chinese"),
        ("Continental", "Continental"),
        ("Desserts", "Desserts"),
        ("Sutta", "Sutta"),
    )
    cuisine=models.CharField(choices=cuisines, max_length=30, default="None")
    # img=models.CharField(max_length=100, default="None") #change to ImageField
    img=models.ImageField(upload_to='img/', null=True, blank=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name_plural = "Menu"


class Order(models.Model):
    user=models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered=models.DateField(auto_now_add=True)
    complete=models.BooleanField(default=False)
    transaction_id=models.CharField(max_length=100, null=True)

    @property
    def get_prep_time(self):
        orderitems=self.orderitem_set.all()
        return max([item.product.prep_time for item in orderitems],default=0)

    @property
    def get_cart_total(self):
        orderitems=self.orderitem_set.all()
        total=sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_final(self):
        orderitems=self.orderitem_set.all()
        total=sum([item.get_total for item in orderitems])
        return total+(0.18*total)

    @property
    def get_cart_tax(self):
        orderitems=self.orderitem_set.all()
        total=sum([item.get_total for item in orderitems])
        return 0.18*total

    @property
    def get_cart_items(self):
        orderitems=self.orderitem_set.all()
        total=sum([item.quantity for item in orderitems])
        return total

    def __str__(self) -> str:
        return str(self.id)

class OrderItem(models.Model):
    product=models.ForeignKey(Menu, on_delete=models.SET_NULL, null=True)
    order=models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity=models.IntegerField(default=0, null=True, blank=True)
    date_added=models.DateField(auto_now_add=True)

    @property
    def get_total(self):
        total=self.product.price*self.quantity
        return total

    def __str__(self) -> str:
        return str(self.id)