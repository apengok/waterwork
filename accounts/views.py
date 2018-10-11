# -*- coding:utf-8 -*-
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse,HttpResponseRedirect
from django.utils.http import is_safe_url
from django.views.generic import CreateView,DetailView,UpdateView,FormView
from .forms import LoginForm,RegisterForm ,UserDetailChangeForm  #,GuestForm
from waterwork.mixins import NextUrlMixin, RequestFormAttachMixin
from sysm.models import Personalized
# Create your views here.

#LoginRequiredMixin,
class AccountHomeView(LoginRequiredMixin, DetailView):
    template_name = 'accounts/home.html'
    def get_object(self):
        return self.request.user

class UserDetailUpdateView(LoginRequiredMixin, UpdateView):
    form_class = UserDetailChangeForm
    template_name = 'accounts/detail-update-view.html'

    def get_object(self):
        return self.request.user

    def get_context_data(self, *args, **kwargs):
        context = super(UserDetailUpdateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Change Your Account Details'
        return context

    def get_success_url(self):
        return reverse("account:home")

# def guest_register_view(request):
#     form = GuestForm(request.POST or None)
#     context = {
#         "form":form
#     }
#     next_ = request.GET.get('next')
#     next_post = request.POST.get('next')
#     redirect_path = next_ or next_post or None
#     if form.is_valid():
#         email = form.cleaned_data.get("email")
#         new_guest_email = GuestEmail.objects.create(email=email)
#         request.session['guest_email_id'] = new_guest_email.id
#         if is_safe_url(redirect_path,request.get_host()):
#             return redirect(redirect_path)
#         else:
#             return redirect("/register/")
        
#     return redirect("/register")


# def login_page(request):
#     form = LoginForm(request.POST or None)
#     context = {
#         "form":form
#     }
#     next_ = request.GET.get('next')
#     next_post = request.POST.get('next')
#     redirect_path = next_ or next_post or None
#     if form.is_valid():
#         username = form.cleaned_data.get("username")
#         password = form.cleaned_data.get("password")
#         user = authenticate(request,username=username,password=password)
#         if user is not None:
#             login(request,user)
#             try:
#                 del request.session['guest_email_id']
#             except:
#                 pass
#             if is_safe_url(redirect_path,request.get_host()):
#                 return redirect(redirect_path)
#             else:
#                 return redirect("/")
#         else:
#             #return an 'invalid login' error message.
#             print("Error")
#     return render(request,"accounts/login.html",context)

# class LoginView(FormView):
#     form_class = LoginForm
#     template_name = 'accounts/login.html'
#     success_url = '/'

#     def form_valid(self,form):
#         request = self.request
#         next_ = request.GET.get('next')
#         next_post = request.POST.get('next')
#         redirect_path = next_ or next_post or None
#         username = form.cleaned_data.get("username")
#         password = form.cleaned_data.get("password")
#         user = authenticate(request,username=username,password=password)
#         if user is not None:
#             login(request,user)
#             try:
#                 del request.session['guest_email_id']
#             except:
#                 pass
#             if is_safe_url(redirect_path,request.get_host()):
#                 return redirect(redirect_path)
#             else:
#                 return redirect("/")
#         return super(LoginView,self).form_invalid(form)

# class GuestRegisterView(NextUrlMixin,  RequestFormAttachMixin, CreateView):
#     form_class = GuestForm
#     default_next = '/register/'

#     def get_success_url(self):
#         return self.get_next_url()

#     def form_invalid(self, form):
#         return redirect(self.default_next)


class LoginView(NextUrlMixin, RequestFormAttachMixin, FormView):
    form_class = LoginForm
    success_url = '/entm/'
    template_name = 'index.html'
    default_next = '/entm/'

    def form_valid(self, form):
        
        user = self.request.user
        p = Personalized.objects.filter(belongto=user.belongto) #.filter(ptype="custom")

        if p.exists():
            next_path = p.first().frontPageMsgUrl
            
            if next_path is None or len(next_path) == 0:
                next_path = self.get_next_url()
        else:
            next_path = self.get_next_url()

        return redirect(to=next_path)
        # return render(self.request,next_path,{})

    



class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = '/login/'

# def register_page(request):
#     form = RegisterForm(request.POST or None)
#     context = {
#         "form":form
#     }
#     if form.is_valid():
#         print(form.cleaned_data)
#         username = form.cleaned_data.get("username")
#         email = form.cleaned_data.get("email")
#         password = form.cleaned_data.get("password")
#         new_user = User.objects.create_user(username,email,password)
#         print(new_user)