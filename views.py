from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render ,redirect
from .models import *
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import *
from .filters import   *
def is_valid_queryparam(param):
    return param != '' and param is not None


def filter(request):
    qs = Product.objects.all()
    brand = request.GET.get('brand')
    prix = request.GET.get('prix')
    catalog = request.GET.get('catalog')


    if is_valid_queryparam(brand) and brand != 'Choose...':
        qs = qs.filter(brand__name=brand)

    if is_valid_queryparam(catalog) and catalog != 'Choose...':
        qs = qs.filter(catalog__title=catalog)


    if is_valid_queryparam(prix):
        if prix == "0":
            qs = qs.filter(price__gt=0)
            qs = qs.filter(price__lt=100000)
        elif prix == "1" :
             qs = qs.filter(price__lt=500)
        elif prix== "2":
            qs = qs.filter(price__lt=1000)
            qs = qs.filter(price__gt=500)
        elif prix =="3"  :
            qs = qs.filter(price__lt=2000)
            qs = qs.filter(price__gt=1000)
        elif prix=="4":
            qs = qs.filter(price__lt=5000)
            qs = qs.filter(price__gt=2000)

        elif prix=="5":
            qs = qs.filter(price__lt=10000)
            qs = qs.filter(price__gt=5000)

        elif prix=="6":
            qs = qs.filter(price__gt=10000)



    return qs


def homepage(request):
    brands = Brand.objects.all()
    catalogues = Catalogue.objects.all()
    products = Product.objects.all()
    filter = Productfilter(request.GET, queryset=products)
    products = filter.qs

    context = {'filter':filter,'brands' : brands,'catalogues':catalogues,'products':products}
    return render(request, 'Shop/HomePage.html',context)

def brandspage(request):
    brands = Brand.objects.all()
    context = {'brands' : brands,}
    return render(request, 'Shop/Brands.html',context)

@login_required
def offrepage(request):
    brands = Brand.objects.all()
    product = Product.objects.all()
    offres= Offre.objects.all()
    context = {'brands' : brands,'offres': offres,'product':product}
    return render(request, 'Shop/cart.html',context)
@login_required
def offres(request):
    brands = Brand.objects.all()
    product = Product.objects.all()
    offres= Offre.objects.all()
    context = {'brands' : brands,'offres': offres,'product':product}
    return render(request, 'Shop/offres.html',context)

@login_required
def Conversation(request,offer_id):
    offer = Offre.objects.get(pk=offer_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            conversationmessage = ConversationMessage.objects.create(offer=offer, content=content,created_by=request.user)
            return redirect('Conversation', offer_id=offer_id)
    brands = Brand.objects.all()
    product = Product.objects.all()
    offres= Offre.objects.all()
    context = {'offer': offer ,'brands' : brands,'offres': offres,'product':product}
    return render(request, 'Shop/conversation.html',context)

@login_required
def articles(request):
    brands = Brand.objects.all()
    products = Product.objects.all()
    offres= Offre.objects.all()
    context = {'brands' : brands,'offres': offres,'products':products}
    return render(request, 'Shop/Articles.html',context)

def productdetail(request,product_id):
    product = Product.objects.get(pk=product_id)
    brands = Brand.objects.all()
    context = {'brands' : brands,'product':product}
    return render(request, 'Shop/ProductDetail.html',context)

def cataloguespage(request):
    catalogues = Catalogue.objects.all()
    context = {'catalogues':catalogues,}
    return render(request, 'Shop/Catalogues.html',context)

def boutiquepage(request):
    brands = Brand.objects.all()
    catalogues = Catalogue.objects.all()
    products = Product.objects.all()
    products = filter(request)
    page = request.GET.get('page', 1)
    paginator = Paginator(products, 9)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context = {'brands': brands, 'catalogues': catalogues, 'products': products}
    return render(request, 'Shop/Shop.html',context)


def Shopbycatalogue(request,cata_id):

    mark = Catalogue.objects.get(pk=cata_id)
    catalogues = Catalogue.objects.all()
    products = mark.catalog.all()

    page = request.GET.get('page', 1)

    paginator = Paginator(products, 9)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)


    context = { 'catalogues': catalogues, 'products': products}
    return render(request, 'Shop/ShopByBrand.html', context)

def shopitembrand(request,brand_id):

    mark = Brand.objects.get(pk=brand_id)
    catalogues = Catalogue.objects.all()
    products = mark.brand.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(products, 9)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)


    context = { 'catalogues': catalogues, 'products': products}
    return render(request, 'Shop/ShopByCatalogue.html', context)

from .forms import *

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()

    context = { 'form2':form}
    return render(request, 'Shop/Signin.html',context)


def log_in(request):
    if request.method == 'POST':
        form1 = AuthenticationForm(request=request, data=request.POST)
        if form1.is_valid():
            username = form1.cleaned_data.get('username')
            password = form1.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                 login(request, user)
                 return redirect('home')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form1 = AuthenticationForm()
    context = {'form1': form1}

    return render(request, 'Shop/Login.html', context)

@login_required
def addproduct(request):
    if request.method =='POST'  :

        form = ProductForm(request.POST,request.FILES )
        if form.is_valid():
            form = form.save(commit=False)
            form.by = request.user
            form.save()
            return redirect('home')
    else:
        form = ProductForm()
    brands = Brand.objects.all()
    catalogues = Catalogue.objects.all()
    context = {'catalogues':catalogues, 'brands':brands,'form': form}

    return render(request, 'Shop/AddProduct.html', context)


@login_required
def Modifyproduct(request,product_id):
    product = Product.objects.get(pk=product_id)

    if request.method =='POST'  :

        form = ProductForm(request.POST,request.FILES,instance=product )
        if form.is_valid():
            form = form.save(commit=False)
            product.status = request.POST.get('status')
            form.save()
            return redirect('home')
    else:
        form = ProductForm()
    brands = Brand.objects.all()
    catalogues = Catalogue.objects.all()
    context = {'product': product,'catalogues':catalogues, 'brands':brands,'form': form}

    return render(request, 'Shop/Modifyproduct.html', context)
@login_required
def Deleteproduct(request,product_id):
    product = Product.objects.get(pk=product_id)

    if request.method =='POST'  :
            product.delete()
            return redirect('home')
    else:
        form = ProductForm()
    brands = Brand.objects.all()
    catalogues = Catalogue.objects.all()
    context = {'product': product,'catalogues':catalogues, 'brands':brands,'form': form}

    return render(request, 'Shop/DeleteProduct.html', context)


@login_required
def offredetail(request,product_id):
    product = Product.objects.get(pk=product_id)

    if request.method == 'POST':

        form = OfferForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.produit = product
            form.created_by = request.user
            form.save()
            return redirect('home')
    else:
        form = OfferForm()
    brands = Brand.objects.all()
    catalogues = Catalogue.objects.all()
    context = {'catalogues': catalogues, 'brands': brands,'product':product, 'form': form}
    return render(request, 'Shop/OffreDetail.html', context)




