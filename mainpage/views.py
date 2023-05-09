from django.shortcuts import render, redirect
from .models import Category, Product, Cart
from . import models
from .forms import SearchForm
from telebot import TeleBot
# Create your views here.

bot = TeleBot('6088414804:AAFrP_qUVAovD30UyDB6P46VDhg1ee-cBzA', parse_mode='HTML')

def index(request):
    all_products = models.Product.objects.all()
    search_bar = SearchForm()
    all_categories = models.Category.objects.all()
    context = {'products': all_products,
               'all_categories': all_categories,
               'form': search_bar}
    if request.method == 'POST':
        product_find = request.POST.get('search_product')
        try:
            search_result = models.Product.objects.get(product_name__contains=product_find)
            return redirect(f'/item/{search_result.id}')
        except:
            return redirect('/')
    return render(request,'index.html', context)
def current_products(request, pk):
    pruducts = models.Product.objects.get(id=pk)

    context ={'products': pruducts}
    return render(request, 'current_products.html', context)
def get_exact_category(request, pk):
    exact_category = models.Category.objects.get(id=pk)
    category_products = models.Product.objects.filter(product_category=exact_category)
    return render(request, 'exact_category.html', {'category_products': category_products})
def exact_product(request, pk):
    find_product_from_db = models.Product.objects.get(id=pk)
    context = {'product': find_product_from_db}
    if request.method == 'POST':
        models.Cart.objects.create(user_id=request.user.id,
                                       user_product=find_product_from_db,
                                       user_product_quantity=request.POST.get('user_product_quantity'),
                                       total_for_product=find_product_from_db.product_price*int(request.POST.get('user_product_quantity')))
        return redirect('/cart')
    return render(request, 'exact_product.html', context)

def get_user_cart(request):
    user_cart = models.Cart.objects.filter(user_id=request.user.id)
    context = {'cart': user_cart}
    return render(request, 'user_cart.html', context)

def complete_order(request):
    user_cart = models.Cart.objects.filter(user_id=request.user.id)
    result_message = 'Новый заказ(Сайт)\n'
    total_for_all_cart = 0
    for cart in user_cart:
        result_message = f'<b>{cart.user_product}</b> x {cart.user_product_quantity} = {cart.total_for_product} сум'

        total_for_all_cart = cart.total_for_product

    result_message += f'\b--------\n<b>Итого: {total_for_all_cart} сум</b>'
    bot.send_message(1872376567, result_message)
    return redirect('/')
#'all_categories': all_categories
#    all_categories = models.Category.objects.all()
# from_frontend = request.GET.get("exact_product")
#     print(from_frontend)
#     if from_frontend is not None:
#         all_products = models.Product.objects.filter(product_name__contains = from_frontend)