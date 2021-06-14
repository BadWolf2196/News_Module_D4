from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from datetime import datetime
from .models import Post, Category
from django.shortcuts import render
from django.views import View  # импортируем простую вьюшку
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage  # импортируем класс, позволяющий удобно осуществлять постраничный вывод
from .filters import NewsFilter
from .forms import NewsForm

class NewsList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    ordering = ['-Post_time']
    paginate_by = 1
    form_class = NewsForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = NewsFilter(self.request.GET, queryset=self.get_queryset())
        context['time_now'] = datetime.utcnow()  # добавим переменную текущей даты time_now

        context['categories'] = Category.objects.all()
        context['form'] = NewsForm()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)  # создаём новую форму, забиваем в неё данные из POST-запроса

        if form.is_valid():  # если пользователь ввёл всё правильно и нигде не ошибся, то сохраняем новый товар
            form.save()

        return super().get(request, *args, **kwargs)

class NewsDetailView(DetailView):
    template_name = 'newnews/news_detail.html'
    queryset = Post.objects.all()

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class NewsCreateView(CreateView):
    template_name = 'news_create.html'
    form_class = NewsForm




# дженерик для редактирования объекта
class NewsUpdateView(UpdateView):
    template_name = 'newnews/news_create.html'
    form_class = NewsForm

    # метод get_object мы используем вместо queryset, чтобы получить информацию об объекте, который мы собираемся редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


# дженерик для удаления товара
class NewsDeleteView(DeleteView):
    template_name = 'newnews/news_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'




class Search(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'search'
    queryset = Post.objects.order_by('-Post_time')
    paginate_by = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = NewsFilter(self.request.GET, queryset=self.get_queryset())
        context['time_now'] = datetime.utcnow()  # добавим переменную текущей даты time_now

        context['categories'] = Category.objects.all()
        context['form'] = NewsForm()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)  # создаём новую форму, забиваем в неё данные из POST-запроса

        if form.is_valid():  # если пользователь ввёл всё правильно и нигде не ошибся, то сохраняем новый товар
            form.save()

        return super().get(request, *args, **kwargs)
