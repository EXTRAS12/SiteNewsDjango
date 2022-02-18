from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import BadHeaderError, send_mail
from django.db.models import F
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import DeleteView, DetailView, ListView, UpdateView

from .forms import AddNewsForm, ContactForm
from .models import Category, News, Tag
from .utils import ContextMixin


class HomeNews(ContextMixin, ListView):
    """Главная страница сайта, вывод опубликованных статей"""
    model = News
    template_name = 'main/news_list.html'
    paginate_by = 8

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(HomeNews, self).get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        return context

    def get_queryset(self):
        return News.objects.filter(is_published=True)\
            .select_related('category', 'author')


class NewsByCategory(ContextMixin, ListView):
    """Вывод статей по категориям"""
    template_name = 'main/category.html'
    paginate_by = 8

    def get_queryset(self):
        return News.objects.filter(category__slug=self.kwargs['slug'], is_published=True)\
            .select_related('author', 'category')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(slug=self.kwargs['slug'])
        return context


class NewsByTag(ContextMixin, ListView):
    """Вывод статей по тэгу"""
    template_name = 'main/category.html'
    paginate_by = 8

    def get_queryset(self):
        return News.objects.filter(tags__slug=self.kwargs['slug'], is_published=True)\
            .select_related('author', 'category')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Записи по тегу: ' + str(Tag.objects.get(slug=self.kwargs['slug']))
        return context


class Search(ContextMixin, ListView):
    """Поиск статей"""
    template_name = 'main/search_list_news.html'
    paginate_by = 10

    def get_queryset(self):
        return News.objects.filter(title__icontains=self.request.GET.get('s'), is_published=True)\
            .select_related('author', 'category')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['s'] = f"s={self.request.GET.get('s')}&"
        return context


class NewsDetail(DetailView):
    """Страница конкретной новости"""
    model = News
    context_object_name = 'news_detail'
    template_name = 'main/news_detail.html'
    slug_url_kwarg = 'slug'

    def get_success_url(self):
        return self.request.path

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object.views = F('views') + 1
        self.object.save()
        self.object.refresh_from_db()
        return context


class NewsUpdate(LoginRequiredMixin, UpdateView):
    """Обновление(редактирование) статьи"""
    model = News
    template_name = 'main/add_news.html'
    form_class = AddNewsForm
    slug_url_kwarg = 'slug'

    def dispatch(self, request, *args, **kwargs):
        """ Пользователь может редактировать только свои статьи """
        obj = self.get_object()
        if obj.author != self.request.user:
            return redirect(obj)
        return super(NewsUpdate, self).dispatch(request, *args, **kwargs)


class NewsDelete(LoginRequiredMixin, DeleteView):
    """Удаление статьи"""
    model = News
    success_url = '/my-post/'
    template_name = 'main/news_delete.html'
    slug_url_kwarg = 'slug'

    def dispatch(self, request, *args, **kwargs):
        """ Пользователь может удалять только свои статьи """
        obj = self.get_object()
        if obj.author != self.request.user:
            return redirect(obj)
        return super(NewsDelete, self).dispatch(request, *args, **kwargs)


class MyPost(ContextMixin, LoginRequiredMixin, ListView):
    """Страница мои статьи"""
    template_name = 'main/my_post.html'
    model = News
    paginate_by = 8

    def get_queryset(self):
        return News.objects.filter(author=self.request.user)\
            .select_related('author', 'category')


@login_required
def create_news(request):
    """Добавление статьи на сайт"""
    form = AddNewsForm(request.POST or None,  request.FILES)
    if request.method == "POST":
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            form.save_m2m()
            return redirect('/')
    return render(request, 'main/add_news.html', locals())


def contacts(request):
    """Страница 'контакты', форма отправки сообщений на емэил"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = "Сообщение"
            body = {
                'name': form.cleaned_data['name'],
                'email': form.cleaned_data['email'],
                'message': form.cleaned_data['message'],
            }
            message = "\n".join(body.values())
            try:
                send_mail(subject, message,
                          'info.moonshine@yandex.ru',
                          ['moonshine-order@yandex.ru'])
            except BadHeaderError:
                return HttpResponse('Найден некорректный заголовок')
            return redirect("home")

    form = ContactForm()
    return render(request, "main/contacts.html", {'form': form})
