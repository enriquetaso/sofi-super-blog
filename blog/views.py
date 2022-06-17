from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.shortcuts import redirect
from django.views import generic

from .forms import PostForm
from .models import Post


class PostListView(generic.ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"

    def get_queryset(self):
        """Return published Post ordering desc"""
        return Post.objects.filter(published_date__lte=timezone.now()).order_by(
            "-published_date"
        )


class PostDetailView(generic.DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"

    def get_queryset(self):
        """Return specific published Post"""
        post = get_object_or_404(Post, pk=self.kwargs["pk"])
        return Post.objects.filter(id=post.id)


class PostDeleteView(generic.DeleteView):
    model = Post
    success_url = reverse_lazy("post_list")


class PostCreateFormView(LoginRequiredMixin, generic.FormView):
    template_name = "blog/post_edit.html"
    form_class = PostForm
    post_pk = None

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.published_date = timezone.now()

        # NOT SURE IF THIS IS CORRECT
        item = form.save()
        self.post_pk = item.pk
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse("post_detail", kwargs={"pk": self.post_pk})


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect("post_detail", pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, "blog/post_edit.html", {"form": form})
