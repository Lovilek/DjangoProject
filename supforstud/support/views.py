from django.forms import model_to_dict
from rest_framework import generics
from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, FormView
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseForbidden, HttpResponseBadRequest, \
    HttpResponseServerError, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.response import Response
from rest_framework.views import APIView

from .form import *
from .models import *
from .serializers import SupportSerializer
from .utils import *

class SupportAPIView(APIView):
    def get(self, request):

        s = Support.objects.all()
        return Response({'posts': SupportSerializer(s, many=True).data})

    def post(self, request):
        serializer = SupportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'post': serializer.data})


    def put(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": "Method PUT not allowed"})

        try:
            instance = Support.objects.get(pk=pk)
        except:
            return Response({"error": "Object does not exists"})

        serializer = SupportSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"post": serializer.data})

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": "Method DELETE not allowed"})


        try:
            instance = Support.objects.get(pk=pk)
        except:
            return Response({"error": "Object does not exists"})
        instance.delete()


        return Response({"post": "delete post " + str(pk)})




# class SupportAPIView(generics.ListAPIView):
#     queryset = Support.objects.all()
#     serializer_class = SupportSerializer
#



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

    model = Support
    template_name = 'support/home.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Support.objects.filter(is_published=True).select_related('cat')

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


class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'support/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Contacts")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('home')





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
    paginate_by = 2
    model = Support
    template_name = 'support/home.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Support.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c= Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title='Category - ' + str(c.name),
                                      cat_selected=c.pk)
        return dict(list(context.items()) + list(c_def.items()))


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'support/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Register")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'support/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Authorization")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')


def pageNotFound(request,exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')

def Forbidden(request,exception):
    return HttpResponseForbidden('<h1>Доступ запрещен </h1>')

def BadRequest(request,exception):
    return HttpResponseBadRequest('<h1>Не правильный запрос </h1>')

def ServerError(request):
    return HttpResponseServerError('<h1>Ошибка сервера </h1>')
