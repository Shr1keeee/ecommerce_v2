from django.http.response import JsonResponse
from django.shortcuts import redirect, render

from django.contrib.auth.decorators import login_required

from store.models import Wishlist, Product

@login_required(login_url='loginpage')
def index(request):
    wishlist = Wishlist.objects.filter(user=request.user)
    context = {'wishlist': wishlist}
    return render(request, "store/wishlist.html", context)

@login_required(login_url='loginpage')
def addtowishlist(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('product_id'))
            product_check = Product.objects.get(id=prod_id)
            if(product_check):
                if(Wishlist.objects.filter(user=request.user, product_id=prod_id)):
                    return JsonResponse({'status': "Товар уже добавлен в избранное"})
                else:
                    Wishlist.objects.create(user=request.user, product_id=prod_id)
                    return JsonResponse({'status': "Товар добавлен в избранное"})
            else:
                return JsonResponse({'status': "Товар не найден"})
        else:
            return JsonResponse({'status': "Необходимо авторизоваться"})
    return redirect('/')        


def deletewishlistitem(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('product_id'))
            if(Wishlist.objects.filter(user=request.user, product_id=prod_id)):
                wishlistitem = Wishlist.objects.get(product_id=prod_id, user=request.user)
                wishlistitem.delete()
                return JsonResponse({'status': "Товар удален из избранного"})
            else:
                return JsonResponse({'status': "Товар не найден в избранном"})
        else:
            return JsonResponse({'status': "Авторизуйтесь для продолжения"})
    return redirect('/')
