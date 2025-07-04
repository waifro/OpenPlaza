from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

from django.shortcuts import render
from .models import Product, ProductImage

from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from .forms import ProductForm, CustomUserCreationForm


# Create your views here.

def home(request):
    products = Product.objects.all()
    return render(request, 'core/homepage.html', {'products': products})

def test_view(request):
    # prendere la prima foto del prodotto dal modello ProductImage
    #first_image =

    return render(request, 'core/test.html', {'first_image': first_image})

def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'core/product_detail.html', {'product': product})

def logout_view(request):
    logout(request)
    return redirect("homepage")

def check_username_availability(request):
    if request.method == 'GET':
        username = request.GET.get("username", None)
        exists = User.objects.filter(username=username).exists()
        return JsonResponse({"available": not exists})

def login_view(request):

    if request.user.is_authenticated:
        return redirect("user_profile", username=request.user.username)

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
        form = ProductForm(request.POST)
        images = request.FILES.getlist('images')  # <-- tutte le immagini caricate

        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()

            for f in images:
                ProductImage.objects.create(product=product, image=f)

            return redirect('homepage')
    else:
        form = ProductForm()

    return render(request, 'core/create_product.html', {'form': form})

def user_profile_view(request, username):
    user = get_object_or_404(User, username=username)
    products = Product.objects.filter(seller=user)  # se vuoi mostrare i suoi articoli
    return render(request, 'core/user_profile.html', {'user_profile': user, 'products': products})

def search_results_view(request):
    query = request.GET.get('q')
    results = Product.objects.filter(
        Q(name__icontains=query) | Q(description__icontains=query)
    ) if query else Product.objects.none()
    return render(request, 'search_results.html', {'products': results, 'query': query})