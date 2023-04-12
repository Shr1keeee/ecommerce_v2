from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages

from django.contrib.auth.decorators import login_required

from store.models import Product, Cart

def addtocart(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('product_id'))
            product_check = Product.objects.get(id=prod_id)
            if(product_check):
                if(Cart.objects.filter(user=request.user, product_id=prod_id)):
                    return JsonResponse({'status': "Товар уже в корзине"})
                else:
                    
                    Cart.objects.create(user=request.user, product_id=prod_id, product_qty=1)
                    return JsonResponse({'status': "Товар добавлен в корзину"})
            else:
                return JsonResponse({'status': "Продукт не найден"})
        else:
            return JsonResponse({'status': "Авторизуйтесь для продолжения"})

    return redirect('/')

@login_required(login_url='loginpage')
def viewcart(request):
    cart = Cart.objects.filter(user=request.user)
    context = {'cart': cart}
    return render(request, "store/cart.html", context)

@login_required(login_url='loginpage')
def updatecart(request):
    if request.method == 'POST':
        prod_id = int(request.POST.get('product_id'))
        if(Cart.objects.filter(user=request.user, product_id=prod_id)):
            prod_qty = int(request.POST.get('product_qty'))
            cart = Cart.objects.get(product_id=prod_id, user=request.user)
            cart.product_qty = prod_qty
            cart.save()
            return JsonResponse({'status': "Запись обновлена"})
    return redirect('/')

@login_required(login_url='loginpage')
def deletecartitem(request):
    if request.method == 'POST':
        prod_id = int(request.POST.get('product_id'))
        if(Cart.objects.filter(user=request.user, product_id=prod_id)):
            cartitem = Cart.objects.get(product_id=prod_id, user=request.user)
            cartitem.delete()
            return JsonResponse({'status': "Продукт успешно удален"})
    return redirect('/')