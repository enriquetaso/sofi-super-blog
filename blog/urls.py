from django.urls import path
from . import views

urlpatterns = [
    path("", views.PostListView.as_view(), name="post_list"),
    path("post/<int:pk>/", views.PostDetailView.as_view(), name="post_detail"),
    path("post/new/", views.PostCreateFormView.as_view(), name="post_new"),
    path("post/<int:pk>/edit/", views.post_edit, name="post_edit"),
    path("tags/<int:tag_id>/", views.list_posts_by_tag, name="tag"),
]
