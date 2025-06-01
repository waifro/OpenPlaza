from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

from django.shortcuts import render
from .models import Product

from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import ProductForm, CustomUserCreationForm


# Create your views here.

def home(request):
    products = Product.objects.all()
    return render(request, 'core/homepage.html', {'products': products})

def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'core/product_detail.html', {'product': product})

def logout_view(request):
    logout(request)
    return redirect("homepage")

def check_username_availability(request):
    if request.method == 'GET':
        username = request.GET.get("username", None)
        print("username ricevuto: ", username)
        exists = User.objects.filter(username=username).exists()
        return JsonResponse({"available": not exists})

def login_view(request):

    if request.user.is_authenticated:
        return redirect("homepage")

    error = None

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("homepage")
        else:
            error = "Username e/o password non validi"

    return render(request, "core/login.html", {"error": error})

def register_view(request):

    if request.user.is_authenticated:
        return redirect("homepage")

    form = None
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm() #mostra il form vuoto se l'utente ha aperto la pagina (GET e non POST)

    return render(request, "core/register.html", {"form": form})

def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            return redirect('homepage')
    else:
        form = ProductForm()

    return render(request, 'core/create_product.html', {'form': form})
