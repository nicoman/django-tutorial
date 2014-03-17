import logging

from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.contrib.auth.views import login
from apps.blog.models import Post, Comment
from apps.blog.forms import PostForm, CommentForm


def home(request):
    posts = Post.objects.all()[:2]
    return render(request, "blog/home.html", {'posts': posts})


def posts(request):
    posts = Post.objects.all().order_by("-datetime")
    result = {}
    for p in posts:
        result[p] = p.comment_set.all()
    #posts = Post.objects.filter(title__startswith="C")
    return render(request, "blog/posts.html", {'posts': result})


@login_required
def create_post(request):

    form = PostForm(request.POST or None)
    if form.is_valid():  # All validation rules pass
        user = request.user
        post = form.save(commit=False)
        post.author = user
        post.save()
        return redirect(reverse("blog_posts"))

    return render(request, "blog/create_post.html", {'form': form})


def edit_post(request, post_id):
    logging.critical(request.method)
    a_post_instance = get_object_or_404(Post, id=post_id)
    form = PostForm(request.POST or None, instance=a_post_instance)
    if form.is_valid():  # All validation rules pass
        post = form.save()
        return redirect(reverse("blog_posts"))

    return render(request, "blog/edit_post.html", {'form': form})


def post(request, post_id):
    a_post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(post=post_id)
    form = CommentForm()
    return render(request, 'blog/post.html', {'post': a_post, 'comments': comments, 'form': form})


# ---------------------------------------------------
# FORMS EXAMPLES
# ---------------------------------------------------


def create_post_first_aproach(request):
    if request.method == "POST":
        form = PostForm(request.POST)  # A form bound to the POST data
        if form.is_valid():  # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            user = User.objects.all()[0]
            post = form.save(commit=False)
            post.author = user
            post.save()
            return redirect(reverse("blog_posts"))  # Redirect after POST
    else:
        form = PostForm()

    return render(request, "blog/create_post.html", {'form': form})


@login_required
def comment_post(request, post_id):
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        post = get_object_or_404(Post, id=post_id)
        comment.post = post
        comment.save()
        return redirect(reverse("blog_posts"))

    return render(request, "blog/comment_post.html", {'form': form})


