from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseForbidden, HttpResponseBadRequest, \
    HttpResponseServerError, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin

from .form import *
from .models import *
from .utils import *



# def index(request):
#
#     context = {
#         'menu': menu,
#         'title': 'Main page',
#         'cat_selected': 0,
#
#     }
#
#     return render(request, 'support/home.html', context=context)

class SupportHome(DataMixin, ListView):
    paginate_by = 2
    model = Support
    template_name = 'support/home.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Support.objects.filter(is_published=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Main page")
        return dict(list(context.items()) + list(c_def.items()))



def about(request):
    contact_list = Support.objects.all()
    paginator = Paginator(contact_list, 3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'support/aboutUs.html', {'page_obj': page_obj, 'menu': menu, 'title': 'About'})


def news(request):
    return render(request, 'support/news.html', {'menu': menu, 'title': 'News'})


# def addpage(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#     else:
#         form = AddPostForm()
#     return render(request, 'support/addpage.html', {'form': form, 'menu': menu, 'title': 'Add page'})

class AddPage(LoginRequiredMixin,DataMixin,CreateView):
    form_class = AddPostForm
    template_name = 'support/addpage.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Add page")
        return dict(list(context.items()) + list(c_def.items()))


def contact(request):
    return HttpResponse("Our contacts")

def login(request):
    return HttpResponse("Log in")


# def show_post(request, post_slug):
#     post = get_object_or_404(Support, slug=post_slug)
#
#     context = {
#         'post': post,
#         'menu': menu,
#         'title': post.title,
#         'cat_selected': post.cat_id,
#     }
#
#     return render(request, 'support/post.html', context=context)

class ShowPost(DataMixin,DetailView):
    model = Support
    template_name = 'support/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'],cat_selected=context['post'].cat_id)
        return dict(list(context.items()) + list(c_def.items()))





# def show_category(request, cat_id):
#
#
#     context = {
#         'menu': menu,
#         'title': 'Show categories',
#         'cat_selected': cat_id,
#     }
#
#     return render(request, 'support/home.html', context=context)

class SupportCategory(DataMixin,ListView):
    model = Support
    template_name = 'support/home.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Support.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Category - ' + str(context['posts'][0].cat),
                                      cat_selected=context['posts'][0].cat_id)
        return dict(list(context.items()) + list(c_def.items()))



def pageNotFound(request,exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')

def Forbidden(request,exception):
    return HttpResponseForbidden('<h1>Доступ запрещен </h1>')

def BadRequest(request,exception):
    return HttpResponseBadRequest('<h1>Не правильный запрос </h1>')

def ServerError(request):
    return HttpResponseServerError('<h1>Ошибка сервера </h1>')
