from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Snippet, Language
from .forms import SnippetForm
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.utils.decorators import method_decorator
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
from django.utils.safestring import mark_safe
from django.db.models import Q

# class SnippetAdd
@method_decorator(login_required, name='dispatch')
class SnippetAdd(View):
    def get(self, request):
        form = SnippetForm()
        return render(request, 'snippets/snippet_form.html', {'form': form})

    def post(self, request):
        form = SnippetForm(request.POST)
        if form.is_valid():
            snippet = form.save(commit=False)
            snippet.user = request.user
            snippet.save()
            messages.success(request, 'Snippet creado con éxito.')
            return redirect('user_snippets', snippet.user) 
        return render(request, 'snippets/snippet_form.html', {'form': form})

# class SnippetEdit
@method_decorator(login_required, name='dispatch')
class SnippetEdit(View):
    def get(self, request, id):
        snippet = get_object_or_404(Snippet, id=id, user=request.user)
        form = SnippetForm(instance=snippet)
        return render(request, 'snippets/snippet_form.html', {'form': form})

    def post(self, request, id):
        snippet = get_object_or_404(Snippet, id=id, user=request.user)
        form = SnippetForm(request.POST, instance=snippet)
        if form.is_valid():
            form.save()
            messages.success(request, 'Snippet actualizado con éxito.')
            return redirect('user_snippets', snippet.user)
        return render(request, 'snippets/snippet_form.html', {'form': form})

# class SnippetDelete
@method_decorator(login_required, name='dispatch')
class SnippetDelete(View):
    def get(self, request, id,):
        snippet = get_object_or_404(Snippet, id=id, user=request.user)
        snippet.delete()
        messages.success(request, 'Snippet eliminado con éxito.')
        return redirect('user_snippets', snippet.user)

# class SnippetDetails
class SnippetDetails(View):
    def get(self, request, *args, **kwargs):
        snippet_id = self.kwargs["snippet_id"]
        snippet = get_object_or_404(Snippet, id=snippet_id)
        lexer = get_lexer_by_name(snippet.language.name)
        formatter = HtmlFormatter()
        highlighted_code = highlight(snippet.snippet, lexer, formatter)

        return render(request, "snippets/snippet.html", {"snippet": snippet, "highlighted_code": mark_safe(highlighted_code)})

# class UserSnippets
class UserSnippets(View):
    def get(self, request, *args, **kwargs):
        username = self.kwargs["username"]
        user_snippets = Snippet.objects.filter(user__username=username)

        return render(
            request,
            "snippets/user_snippets.html",
            {"snippetUsername": username, "snippets": user_snippets},
        )

# class SnippetsByLanguage
class SnippetsByLanguage(View):
    def get(self, request, *args, **kwargs):
        language_name = self.kwargs["language"]
        snippet_language = Snippet.objects.filter(language__name=language_name)
        return render(
            request,
            "snippets/snippet_list.html",
            {"snippetlanguage": language_name, "snippets": snippet_language},
        )

    
# class Login
class Login(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'snippets/login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('user_snippets', user.username) 
        return render(request, 'snippets/login.html', {'form': form})

# class Logout
class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('index')

# class Index
class Index(View):
    def get(self, request, *args, **kwargs):
        snippets = Snippet.objects.filter(public=True)
        return render(request, "index.html", {"snippets": snippets})

