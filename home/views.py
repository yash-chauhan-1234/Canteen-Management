from multiprocessing import context
import os
from django.shortcuts import render, redirect
from .models import Menu, Order, OrderItem
from .forms import SignupForm, MenuForm
from django.contrib.auth import login,authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json

# Create your views here.
def home(request):
    return render(request, 'index.html') 

def contacts(request):
    return render(request, 'contacts.html')

def login_users(request):
    if request.method=="POST":
        sap = request.POST['username']
        passw = request.POST['password']
        user = authenticate(request, username=sap, password=passw)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return redirect("home")

        else:
            # Return an 'invalid login' error message.
            messages.error(request, "There was an error logging in")
            return redirect("login")
    else:
        return render(request, "login.html")

def logout_users(request):
    logout(request)
    return redirect("home")

def product(request,name):
    data=Menu.objects.get(name=name)
    context={"data":data}
    return render(request, 'product.html', context) 


def products(request):
    menu= Menu.objects.all()
    context={"menu":menu}
    return render(request, 'products.html',context) 

def products_cuis(request, cuis):
    try:
        menu= Menu.objects.filter(cuisine=cuis)
        context={"menu":menu}
    except:
        context={"menu": None}
    return render(request, 'products.html',context)

@login_required(login_url='login')
def shoppingcart(request):
    order, created=Order.objects.get_or_create(user=request.user, complete=False)
    item=order.orderitem_set.all()

    
    context={"items":item, "order":order}   

    return render(request, 'shopping-cart.html', context) 


def signup(request):
    if request.method=="POST":
        form=SignupForm(request.POST)
        if form.is_valid():
            new_user=form.save()

            login(request, new_user)

            return redirect("home")
    else:
        form=SignupForm()
    
    return render(request, "signup.html", {"form":form})



#crud ops
@login_required(login_url='login')
def add_product(request):
    if request.user.is_superuser:
        form=MenuForm()
        if request.method=='POST':
            data=MenuForm(request.POST, request.FILES)
            if data.is_valid():
                data.save()
                #print message success
                return redirect('products')
            else:
                #print message failure
                return redirect('home')
        
        return render(request, 'crud/add.html', {'form':form})
    else:
        return redirect('home')

@login_required(login_url='login')
def update_product(request, name):
    if request.user.is_superuser:
        data=Menu.objects.get(name=name)
        update_form=MenuForm(request.POST or None, request.FILES or None, instance=data)
        if update_form.is_valid():

            image_path = data.img.url
            if os.path.exists(image_path):
                os.remove(image_path)
            update_form.save()

            #print success message
            return redirect('products')
        

        return render(request, 'crud/update.html', {'form': update_form})
    else:
        return redirect('home')

@login_required(login_url='login')
def delete_product(request, name):
    if request.user.is_superuser:
        data=Menu.objects.get(name=name)
        data.delete()
        return redirect('products')
    else:
        return redirect('home')


def update_item(request):
    data=json.loads(request.body)
    productId=data['productId']
    action=data['action']
    # print(productId)
    # print(action)

    customer=request.user
    product=Menu.objects.get(id=productId)
    order, created=Order.objects.get_or_create(user=customer, complete=False)
    orderItem, created=OrderItem.objects.get_or_create(order=order, product=product)
    if action=='add':
        # for i in range(1):
        print("Old: ",orderItem.quantity)
        orderItem.quantity=orderItem.quantity+1
        print("New: ", orderItem.quantity)
    elif action=='remove':
        # for i in range(1):
        print("Old Removed: ",orderItem.quantity)
        orderItem.quantity=orderItem.quantity-1
        print("New Removed: ", orderItem.quantity)


    orderItem.save()

    if orderItem.quantity<=0:
        orderItem.delete()


    return redirect('shoppingcart')