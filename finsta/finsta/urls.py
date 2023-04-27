"""finsta URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',views.SignUpView.as_view(),name="register"),
    path('',views.SigninView.as_view(),name="signin"),
    path('index/',views.IndexView.as_view(),name="index"),
    path("profile/<int:pk>",views.EditProfileView.as_view(),name="edit-profile"),
    path('logout/',views.signout_view,name="signout"),
    path('posts/<int:pk>/like/',views.add_like_view,name="addlike"),
    path('posts/<int:pk>/comment/add',views.add_comment_view,name="addcomment"),
    path('comments/<int:pk>/remove/',views.comment_remove_view,name="remove_comment"),
    path('profiles/<int:pk>/',views.profile_detail_view.as_view(),name="profile_detail"),
    path('profiles/<int:pk>/coverpic/change/',views.change_cover_pic_view,name="coverpic_change"),
    path('profiles/<int:pk>/profile_pic/change/',views.change_profile_pic_view,name="profilepic_change"),
    path('profiles/all/',views.ProfileListView.as_view(),name="profile-list"),
    path('profiles/<int:pk>/follow/',views.follow_view,name="follow"),
    path('profiles/<int:pk>/unfollow/',views.unfollow_view,name="unfollow"),
    path('profiles/following/all/',views.FollowingListView.as_view(),name="following-list"),
    path('posts/<int:pk>/remove/',views.post_delete_view,name="post-remove"),


    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
