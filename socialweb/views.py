from django.shortcuts import render,redirect
from socialweb.forms import RegisterationForm,LoginForm,UserProfileForm,PostForm
from django.views.generic import View,TemplateView,UpdateView,CreateView,ListView
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from socialweb.models import Post,UserProfile,Comments
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
def signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            return redirect("signin")
        else:
            return fn(request,*args,**kwargs)
    return wrapper
disc=[signin_required,never_cache]

class SignUpView(View):                                           #register
    def get(self,request,*args,**kwargs):
        form=RegisterationForm()
        return render(request,"signup.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=RegisterationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("signin")
        else:
            return render(request,"signup.html",{"form":form})


class LogInView(View):
    def get(self,request,*args,**kwargs):
        form=LoginForm()
        return render(request,"signin.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            print(uname,pwd)
            usr=authenticate(request,username=uname,password=pwd)
            if usr:
                login(request,usr)
                return redirect("home")       #profile
            else:
                return render(request,"signin.html",{"form":form})
        else:
            return render(request,"signin.html",{"form":form})
        
@method_decorator(disc,name="dispatch")
class IndexView(CreateView,ListView):
    model=Post
    form_class=PostForm
    template_name="index.html"
    success_url=reverse_lazy("home")
    context_object_name="post"

    def form_valid(self,form):
        form.instance.user=self.request.user
        return super().form_valid(form)
        
@method_decorator(disc,name="dispatch")
class ProfileCreateView(View):
    def get(self,request,*args,**kwargs):
        form=UserProfileForm()
        return render(request,"profile-create.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        form=UserProfileForm(request.POST,files=request.FILES)
        if form.is_valid():
            usr=User.objects.get(username=request.user.username)
            form.instance.user=usr
            form.save()
            return redirect("home")
        else:
            return render(request,"profile-create.html",{"form":form})

# class UserProfileView(View):
#     def get(self,request,*args,**kwargs):
#         qs=UserProfile.objects.user=request.user
#         return render(request,"profile.html",{"profile":qs})
@method_decorator(disc,name="dispatch")
class SignoutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("signin")
    
@method_decorator(disc,name="dispatch")
class ProfileDetailView(TemplateView):
    template_name="profile-detail.html"

@method_decorator(disc,name="dispatch")
class ProfileUpdateView(UpdateView):
    model=UserProfile
    form_class=UserProfileForm
    template_name="profile-edit.html"
    success_url=reverse_lazy("home")
    pk_url_kwarg="id"

@method_decorator(disc,name="dispatch")
class PostAddView(CreateView,ListView):
    model=Post
    form_class=PostForm
    template_name="index.html"
    success_url=reverse_lazy("home")
    context_object_name="post"

    def form_valid(self,form):
        form.instance.user=self.request.user
        return super().form_valid(form)
    
@method_decorator(disc,name="dispatch")   
class PostDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        Post.objects.get(id=id).delete()
        return redirect("home")
    
@method_decorator(disc,name="dispatch")
class CommentAddView(View):
    def post(self,request,*args,**kwargs):
        pid=kwargs.get("id")
        com=Post.objects.get(id=pid)
        usr=request.user
        cmt=request.POST.get("comments")
        Comments.objects.create(user=usr,post=com,comment=cmt)
        return redirect("home")

 
@method_decorator(disc,name="dispatch")   
class CommentLikeView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        cmt=Comments.objects.get(id=id)
        cmt.likes.add(request.user)
        cmt.save()
        return redirect("home")
    
@method_decorator(disc,name="dispatch")
class CommentLikeRemoveView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        cmt=Comments.objects.get(id=id)
        cmt.likes.remove(request.user)
        cmt.save()
        return redirect("home")

@method_decorator(disc,name="dispatch")
class LikeView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        lik=Post.objects.get(id=id)
        lik.like.add(request.user)
        lik.save()
        return redirect("home")

@method_decorator(disc,name="dispatch")
class DislikeView(View):
      def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        lik=Post.objects.get(id=id)
        lik.like.remove(request.user)
        lik.save()
        return redirect("home")

@method_decorator(disc,name="dispatch")
class PostUpdateView(UpdateView):
    model=Post
    form_class=PostForm
    template_name="post-edit.html"
    success_url=reverse_lazy("home")
    pk_url_kwarg="id"

@method_decorator(disc,name="dispatch")
class CommentDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        cmt=Comments.objects.get(id=id).delete()
        return redirect("home")

