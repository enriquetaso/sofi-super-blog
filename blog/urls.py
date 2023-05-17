from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("resume/", views.resume, name="resume"),
    path("blog/", views.PostListView.as_view(), name="post_list"),
    path("blog/post/<int:pk>/", views.PostDetailView.as_view(), name="post_detail"),
    path("blog/post/new/", views.PostCreateFormView.as_view(), name="post_new"),
    path("blog/post/<int:pk>/edit/", views.post_edit, name="post_edit"),
    path("tags/<int:tag_id>/", views.list_posts_by_tag, name="tag"),
]
