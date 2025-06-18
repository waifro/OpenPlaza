from django import forms
from .models import Product, ProductImage
from django.contrib.auth.models import User

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'price']

class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(label="Conferma Password", widget=forms.PasswordInput(attrs={'placeholder': 'Conferma Password'}))

    class Meta:
        model = User
        fields = ['username']  # solo i campi del modello
        widgets = {'username': forms.TextInput(attrs={'placeholder': 'Scegli un username'})}

    # Metodo di pulizia del secondo campo password (non dentro Meta!)
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Le password non coincidono.")

        return password2

    def clean(self):
        cleaned_data = super().clean()
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get("password1")

        if username and password and username == password:
            raise forms.ValidationError("L'Username e password non possono combaciare.")

        return cleaned_data

    # Metodo save corretto (non dentro Meta!)
    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password1")
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user