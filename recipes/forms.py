from django import forms
from .models import Recipe, Review, Collection, UserProfile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'ingredients', 'instructions',
                  'cooking_time', 'image', 'category', 'is_published']
        widgets = {
            'ingredients': forms.Textarea(attrs={'rows': 5}),
            'instructions': forms.Textarea(attrs={'rows': 8}),
        }

    def clean_cooking_time(self):
        cooking_time = self.cleaned_data.get('cooking_time')
        if cooking_time < 1:
            raise forms.ValidationError("Cooking time must be at least 1 minute.")
        return cooking_time


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4}),
        }


class CollectionForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = ['name', 'description', 'is_public']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'profile_picture']


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email
