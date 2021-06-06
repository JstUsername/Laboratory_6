from .models import Article
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import Http404
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from .forms import RegisterUserForm
from .forms import AuthUserForm
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

def archive(request):
    return render(request, 'archive.html', {"posts": Article.objects.all()})

def get_article(request, article_id):
    try:
        post = Article.objects.get(id=article_id)
        return render(request, 'article.html', {"post": post})
    except Article.DoesNotExist:
        raise Http404

def create_post(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = {
                'text': request.POST["text"], 'title': request.POST["title"]
            }
            if form["text"] and form["title"] and not Article.objects.filter(title=form["title"]).exists():
                Article.objects.create(text=form["text"], title=form["title"], author=request.user)
                return redirect('get_article', article_id=Article.objects.get(text=form["text"], title=form["title"], author=request.user).id)
            else:
                if Article.objects.filter(title=form["title"]).exists() and not (form["text"] and form["title"]):
                    form['errors'] = u"Название статьи не уникально!\nНе все поля заполнены!"
                elif Article.objects.filter(title=form["title"]).exists():
                    form['errors'] = u"Название статьи не уникально!"
                else:
                    form['errors'] = u"Не все поля заполнены!"
                return render(request, 'create_post.html', {'form': form})
        else:
            return render(request, 'create_post.html', {})
    else:
        raise Http404

class RegisterUserView(CreateView):
    model = User
    template_name = 'registration.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('archive')
    def get_success_url(self):
        return self.success_url


class LoginUserView(LoginView):
    template_name = 'autorization.html'
    form_class = AuthUserForm
    success_url = reverse_lazy('archive')
    def get_success_url(self):
        return self.success_url
