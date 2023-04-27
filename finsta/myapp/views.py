from django.shortcuts import render,redirect
from myapp.forms import SignupForm,LoginForm,ProfileEditForm,PostForm,CoverpicForm,ProfilepicForm
from django.urls import reverse_lazy
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.db.models import Q
from django.views.generic import CreateView,View,FormView,TemplateView,UpdateView,ListView,DetailView
from django.contrib import messages
from django.utils.decorators import method_decorator

from myapp.models import UserProfile,Posts,Comments


# Create your views here.

def sign_required(fn):
    def wrapper(request,*args,**kw):
        if not request.user.is_authenticated:
            messages.error(request,"you have to login")
            return redirect("signin")
        return fn(request,*args,**kw)
    return wrapper


class SignUpView(CreateView):
    model=User
    template_name="register.html"
    form_class=SignupForm
    success_url=reverse_lazy("signin")
    
    def form_valid(self,form):
        messages.success(self.request,"account has been created")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request,"failed to create account")
        return super().form_invalid(form)
    
class SigninView(FormView):
    model=User
    template_name="login.html"
    form_class=LoginForm

    # def get(self,request,*args,**kw):
    #     form=self.form_class
    #     return render(request,self.template_name,{"forms":form})


    def post(self,request,*args,**kw):
        form=self.form_class(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            usr=authenticate(request,username=uname,password=pwd)
            if usr:
                login(request,usr)
                messages.success(request,"login success")
                return redirect("index")
        messages.error(request,"invalid credential")
        return render(request,self.template_name,{"forms":form})

@method_decorator(sign_required,name="dispatch")
class IndexView(CreateView,ListView):
    template_name="index.html"
    form_class=PostForm
    model=Posts
    context_object_name="posts"
    success_url=reverse_lazy("index")
    def form_valid(self, form):
        form.instance.user=self.request.user
        return super().form_valid(form)

@method_decorator(sign_required,name="dispatch")
class EditProfileView(UpdateView):
    model=UserProfile
    template_name="profile_edit.html"
    form_class=ProfileEditForm
    success_url=reverse_lazy("index")

@method_decorator(sign_required,name="dispatch")
def signout_view(request,*args,**kw):
    logout(request)
    return redirect("signin")

@method_decorator(sign_required,name="dispatch")
def add_like_view(request,*args,**kw):
    id=kw.get("pk")
    post_obj=Posts.objects.get(id=id)
    post_obj.liked_by.add(request.user)
    return redirect("index")

# localhost:8000/posts/{id}/comments/add/
@method_decorator(sign_required,name="dispatch")
def add_comment_view(request,*args,**kw):
    id=kw.get("pk")
    post_obj=Posts.objects.get(id=id)
    comment=request.POST.get("comment")
    Comments.objects.create(user=request.user,post=post_obj,comment_text=comment)
    return redirect("index")
# localhost:8000/comments/{id}/remove/


@method_decorator(sign_required,name="dispatch")
def comment_remove_view(request,*args,**kw):
    id=kw.get("pk")
    comment_obj=Comments.objects.get(id=id)
    if request.user==comment_obj.user:
        comment_obj.delete()
        return redirect("index")
    else:
        messages.error(request,"plz contact admin")
        return redirect("signin")
    
@method_decorator(sign_required,name="dispatch")    
class profile_detail_view(DetailView):
    model=UserProfile
    template_name="profile.html"
    context_object_name="profile"

@method_decorator(sign_required,name="dispatch")
def change_cover_pic_view(request,*args,**kw):
    id=kw.get("pk")
    prof_obj=UserProfile.objects.get(id=id)
    form=CoverpicForm(instance=prof_obj,data=request.POST,files=request.FILES)
    if form.is_valid():
        form.save()
        return redirect("profile_detail",pk=id)
    return redirect("profile_detail",pk=id)

@method_decorator(sign_required,name="dispatch")
def change_profile_pic_view(request,*args,**kw):
    id=kw.get("pk")
    prof_obj=UserProfile.objects.get(id=id)
    form=ProfilepicForm(instance=prof_obj,data=request.POST,files=request.FILES)
    if form.is_valid():
        form.save()
        return redirect("profile_detail",pk=id)
    return redirect("profile_detail",pk=id)

@method_decorator(sign_required,name="dispatch")
class ProfileListView(ListView):
    model=UserProfile
    template_name="profile_list.html"
    context_object_name="profiles"


    def get_queryset(self):
        return UserProfile.objects.exclude(user=self.request.user)
    
    def post(self,request,*args,**kw):
        pname=request.POST.get("username")
        # =,iexact,icontains
        qs=UserProfile.objects.filter(Q(user__username__icontains=pname) | Q(user__first_name__icontains=pname) | Q(user__last_name__icontains=pname))
        return render(request,self.template_name,{"profiles":qs})
    
    # or
    # def get(self,request,*args,**kw):
    #     qs=UserProfile.objects.exclude(user=self.request.user)
    #     return render(request,self.template_name,{"profiles":qs})
@method_decorator(sign_required,name="dispatch")
def follow_view(request,*args,**kw):
    id=kw.get("pk")
    profile_obj=UserProfile.objects.get(id=id)
    user_obj=request.user.profile
    user_obj.following.add(profile_obj)
    user_obj.save()
    return redirect("index")

@method_decorator(sign_required,name="dispatch")
def unfollow_view(request,*args,**kw):
    id=kw.get("pk")
    profile_obj=UserProfile.objects.get(id=id)
    user_obj=request.user.profile
    user_obj.following.remove(profile_obj)
    user_obj.save()
    return redirect("index")

@method_decorator(sign_required,name="dispatch")    
class FollowingListView(ListView):
    model=UserProfile
    template_name="following_list.html"
    context_object_name="profiles"


    def get_queryset(self):
        return UserProfile.objects.exclude(user=self.request.user)
    
def post_delete_view(request,*args,**kw):
    post_id=kw.get("pk")
    post_obj=Posts.objects.get(id=post_id)
    post_obj.delete()
    return redirect("index")
