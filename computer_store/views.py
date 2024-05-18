from django.shortcuts import render, redirect
from . import models
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


@login_required(login_url='log_in')
def index(request):
    admin = User.objects.all()
    entery = models.EnterProduct.objects.all()
    orders = models.OutProduct.objects.all()
    returns = models.ReturnedProduct.objects.all()
    context = {
        'orders': orders,
        'returns': returns,
        'entery': entery,
        'admin': admin,
    }
    return render(request, 'index.html', context)


#Authenticate
def log_in(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'login.html', {'error': 'Username or Password is incorrect'})
        
    else:
        return render(request, 'login.html')
    

def log_out(request):
    logout(request)
    return redirect('log_in')


#Category
@login_required(login_url='log_in')
def category_create(request):
    if request.method == 'POST':
        category = request.POST['category']
        models.Category.objects.create(category=category)
        return redirect('category_list')
    else:
        return render(request, 'category/create.html')


@login_required(login_url='log_in')
def category_list(request):
    category = models.Category.objects.all()
    context = {
        'category': category,
    }
    return render(request, 'category/list.html', context)


@login_required(login_url='log_in')
def category_update(request, code):
    category = models.Category.objects.get(code=code)
    if request.method == 'POST':
        category.category = request.POST['category']
        category.save()
        return redirect('category_list')
    else:
        return render(request, 'category/update.html', {'category': category})
    

@login_required(login_url='log_in')
def category_delete(request, code):
    category = models.Category.objects.get(code=code)
    category.delete()
    return redirect('category_list')


#Product
@login_required(login_url='log_in')
def product_create(request):
    categories = models.Category.objects.all()
    context = {
        categories: categories,
    }

    if request.method == 'POST':
        models.Product.objects.create(
            name=request.POST.get('name'),
            category=models.Category.objects.get(id=request.POST.get('category')),
            quantity=request.POST.get('quantity'),
            price=request.POST.get('price'),
            description=request.POST.get('description'),
            image=request.FILES.get('image')

        )
        return redirect('product_list')
    return render(request, 'product/create.html', context)


@login_required(login_url='log_in')
def product_list(request):
    categories = models.Category.objects.all()
    category_code = request.GET.get('code')

    filtered_items = {}
    for key, value in request.GET.items():
        if value and not value == '0':
            if key == 'start_date':
                key = 'created_at__gte'
            elif key == 'end_date':
                key = 'created_at__lte'
            elif key == 'name':
                key = 'product__name__icontains'
            filtered_items[key] = value

    products = models.Product.objects.filter(**filtered_items)
    context = {
        'products': products,
        'categories': categories,
        'category_code': category_code,
    }
    return render(request, 'product/list.html', context)


@login_required(login_url='log_in')
def product_update(request, code):
    category = models.Category.objects.all()
    product = models.Product.objects.get(code=code)
    context = {
        'category': category,
        'product': product,
    }
    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.category = models.Category.objects.get(id=request.POST.get('category'))
        product.quantity = request.POST.get('quantity')
        product.price = request.POST.get('price')
        product.description = request.POST.get('description')
        product.image = request.FILES.get('image')

        product.save()
        return redirect('product_list')
    return render(request, 'product/update.html', context)


@login_required(login_url='log_in')
def product_delete(request, code):
    product = models.Product.objects.get(code=code)
    product.delete()
    return redirect('product_list')


#EntryProduct
@login_required(login_url='log_in')
def enterproduct_create(request):
    category = models.Category.objects.all()
    products = models.Product.objects.all()
    context = {
        'category': category,
        'products': products,
    }
    if request.method == 'POST':
        models.Entery.objects.create(
            product=models.Product.objects.get(id=request.POST.get('product')),
            quantity=request.POST.get('quantity'),
            date=request.POST.get('date'),
)
        return redirect('enterproduct_list')
    return render(request, 'enter/create.html', context)


@login_required(login_url='log_in')
def enterproduct_list(request):
    category = models.Category.objects.all()
    products = models.Product.objects.filter(category=category)
    category_code = request.GET.get('category_code')
    if category_code:
        filtered_items = {}
        for key, value in request.GET.items():
            if value and not value == '0':
                if key == 'start_date':
                    key = 'date__gte'
                elif key == 'end_date':    
                    key = 'date__lte'
                elif key == 'name':
                    key = 'product__name__icontains'
                filtered_items[key] = value

        enteries = models.Entery.objects.filter(**filtered_items)
    context = {
        'products': products,
        'enteries': enteries,
        'category': category,
        'category_code': category_code,
    }
    return render(request, 'enter/list.html', context)


#ReturnProduct
@login_required(login_url='log_in')
def returnproduct_create(request):
    category = models.Category.objects.all()
    products = models.Product.objects.all()
    context = {
        'category': category,
        'products': products,
    }

    if request.method == 'POST':
        models.ReturnedProduct.objects.create(
            product=models.Product.objects.get(id=request.POST.get('product')),
            quantity=request.POST.get('quantity'),
            date=request.POST.get('date'),
        )
        return redirect('returnproduct_list')
    
    return render(request, 'return/create.html', context)


@login_required(login_url='log_in')
def returnproduct_list(request):
    category = models.Category.objects.all()
    product = models.Product.filter(category=category)
    returns = models.ReturnedProduct.filter(product=product)
    context = {
        'returns': returns,
        'category': category,
        'product': product,
    }
    return render(request, 'return/list.html', context)



        

        
