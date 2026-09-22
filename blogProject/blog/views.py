from django.core.paginator import EmptyPage, Paginator, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from blogProject.blog.models import Post


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/blog/list.html'


def post_detail(request, year, month, day, post):

    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )

    return render(
        request,
        'blog/blog/detail.html',
        {'post': post}
    )
