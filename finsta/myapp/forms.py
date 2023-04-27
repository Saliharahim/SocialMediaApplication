from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from myapp.models import UserProfile,Posts

class SignupForm(UserCreationForm):

    class Meta:
        model=User
        fields=["first_name","last_name","email","username","password1","password2"]

class LoginForm(forms.Form):
        username=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
        password=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))

class ProfileEditForm(forms.ModelForm):
     
     class Meta:
          model=UserProfile
          fields=["profile_pic","bio","address","dob"]
          widgets={
                "profile_pic":forms.FileInput(attrs={"class":"form-control"}),
                "bio":forms.TextInput(attrs={"class":"form-control"}),
                "address":forms.Textarea(attrs={"class":"form-control"}),
                "dob":forms.DateInput(attrs={"class":"form-control","type":"date"})
        }
          
class PostForm(forms.ModelForm):
     
     class Meta:
          model=Posts
          fields=["title","image"]

class CoverpicForm(forms.ModelForm):
     
     class Meta:
          model=UserProfile
          fields=["cover_pic"]

class ProfilepicForm(forms.ModelForm):
     
     class Meta:
          model=UserProfile
          fields=["profile_pic"]
