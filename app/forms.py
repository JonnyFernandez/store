from django import forms
from .models import AppCategory, AppProduct


class PostForm(forms.ModelForm):
    class Meta:
        model = AppProduct
        fields = [
            "name",
            "description",
            "imagen",
            "price",
            "stock",
            "category",
            "offer",
        ]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "ingresa name"}
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "ingresa descripción",
                    "rows": 3,  # Número de filas
                    "cols": 40,  # Número de columnas (ancho)
                }
            ),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = AppCategory
        fields = ["name"]


class SearchForm(forms.Form):
    title = forms.CharField(max_length=100, required=False)
    category = forms.ModelChoiceField(
        queryset=AppCategory.objects.all(), required=False
    )
