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
            "offer",
            "category",
        ]


class CategoryForm(forms.ModelForm):
    class Meta:
        model = AppCategory
        fields = ["name"]


class SearchForm(forms.Form):
    title = forms.CharField(max_length=100, required=False)
    category = forms.ModelChoiceField(
        queryset=AppCategory.objects.all(), required=False
    )
