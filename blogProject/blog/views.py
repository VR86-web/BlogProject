from django.core.paginator import EmptyPage, Paginator, PageNotAnInteger
from django.views.decorators.http import require_POST
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from blogProject.blog.models import Post
from blogProject.blog.forms import EmailPostForm, CommentForm


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

    comments = post.comments.filter(active=True)

    form = CommentForm()

    return render(
        request,
        'blog/blog/detail.html',
        {
            'post': post,
            'comments': comments,
            'form': form
        }
    )

def post_share(request, post_id):

    post = get_object_or_404(
        Post,
        id = post_id,
        status = Post.Status.PUBLISHED
    )

    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url()
                )
            subject = (
                f"{cd['name']} ({cd['email']}) "
                f"recommends you read {post.title}"
            )
            message = (
                f"Read {post.title} at {post_url}\n\n"
                f"{cd['name']}\'s comments: {cd['comments']}"
            )
            send_mail(
                subject=subject,
                message=message,
                from_email=None,
                recipient_list=[cd['to']]
            )
            sent = True

    else:
        form = EmailPostForm()

    return render(
        request,
        'blog/blog/share.html',
        {
            'post' : post,
            'form' : form,
            'sent' : sent
        }
    )

@require_POST
def post_comment(request, post_id):

    post = get_object_or_404(
        Post,
        id=post_id,
        status=Post.Status.PUBLISHED
    )

    comment = None

    form = CommentForm(data=request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()

    return render(
        request,
        'blog/blog/comment.html',
        {
            'post' : post,
            'form' : form,
            'comment' : comment
        }
    )
