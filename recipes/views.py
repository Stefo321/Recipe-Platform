from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .models import Recipe, Category, Review, Collection, UserProfile
from .forms import RecipeForm, ReviewForm, CollectionForm, UserProfileForm
from django.db.models import Q


# Public Views
def home(request):
    recipes = Recipe.objects.filter(is_published=True).order_by('-created_at')[:6]
    categories = Category.objects.all()
    return render(request, 'recipes/home.html', {
        'recipes': recipes,
        'categories': categories
    })


class RecipeListView(ListView):
    model = Recipe
    template_name = 'recipes/recipe_list.html'
    context_object_name = 'recipes'
    paginate_by = 9

    def get_queryset(self):
        queryset = Recipe.objects.filter(is_published=True)

        # Get search query and category from URL
        search_query = self.request.GET.get('search')
        category = self.request.GET.get('category')

        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(ingredients__icontains=search_query)
            )
        if category:
            queryset = queryset.filter(category__name=category)

        return queryset.order_by('-created_at')


class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'recipes/recipe_detail.html'
    context_object_name = 'recipe'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['review_form'] = ReviewForm()
        return context


# Protected Views (require login)
class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipes/recipe_form.html'
    success_url = reverse_lazy('recipe-list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class RecipeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipes/recipe_form.html'

    def test_func(self):
        recipe = self.get_object()
        return self.request.user == recipe.author


class RecipeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Recipe
    success_url = reverse_lazy('recipe-list')
    template_name = 'recipes/recipe_confirm_delete.html'

    def test_func(self):
        recipe = self.get_object()
        return self.request.user == recipe.author


@login_required
def add_review(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.recipe = recipe
            review.user = request.user
            review.save()
    return redirect('recipe-detail', pk=recipe_id)


# Profile Views
# class UserProfileView(LoginRequiredMixin, DetailView):
#     model = UserProfile
#     template_name = 'recipes/profile.html'
#     context_object_name = 'profile'
#
#     def get_object(self):
#         return get_object_or_404(UserProfile, user=self.request.user)
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['user_recipes'] = Recipe.objects.filter(author=self.request.user).order_by('-created_at')
#         return context


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user.userprofile)
    return render(request, 'recipes/edit_profile.html', {'form': form})


# Collection Views
class CollectionCreateView(LoginRequiredMixin, CreateView):
    model = Collection
    form_class = CollectionForm
    template_name = 'recipes/collection_form.html'
    success_url = reverse_lazy('collections')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)
