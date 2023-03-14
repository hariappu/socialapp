from django.urls import path
from socialweb import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    path("register/",views.SignUpView.as_view(),name="signup"),
    path("",views.LogInView.as_view(),name="signin"),
    path("home/",views.IndexView.as_view(),name="home"),
    path("profile/add",views.ProfileCreateView.as_view(),name="profile-create"),
    path("profile/",views.ProfileDetailView.as_view(),name="profile-detail"),
    path("signout",views.SignoutView.as_view(),name="logout"),
    path("profile/<int:id>/change",views.ProfileUpdateView.as_view(),name="profile-edit"),
    path("post/add",views.PostAddView.as_view(),name="post-add"),
    path("post/<int:pk>/remove",views.PostDeleteView.as_view(),name="post-delete"),
    path("post<int:id>/like/add",views.LikeView.as_view(),name="like"),
    path("post<int:id>/comments/add",views.CommentAddView.as_view(),name="comment-add"),
    path("post/<int:id>/change",views.PostUpdateView.as_view(),name="post-edit"),
    path("post<int:id>/like/remove",views.DislikeView.as_view(),name="dislike"),
    path("comment<int:id>/like/add",views.CommentLikeView.as_view(),name="add-like"),
    path("comments<int:id>/like/remove",views.CommentLikeRemoveView.as_view(),name="remove-like"),
    path("comment<int:pk>/remove",views.CommentDeleteView.as_view(),name="comment-delete"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)