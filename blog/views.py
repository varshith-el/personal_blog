from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from blog.forms import CommentForm,PostForm

from blog.models import Post, Comment

def blog_index(request):
    posts = Post.objects.all().order_by("-created_on")

    context = {
        "posts": posts,
    }
    return render(request,"blog/index.html", context)



def blog_category(request,Category):
    posts = Post.objects.filter(
        categories__name__contains=Category
    ).order_by("-created_on")
    context = {
        "category":Category,
        "posts": posts,
    }
    return render(request, "blog/category.html", context)


def blog_detail(request, pk):
    post = Post.objects.get(pk=pk)
    form = CommentForm()
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment(
                author=form.cleaned_data["author"],
                body=form.cleaned_data["body"],
                post=post,
            )
            comment.save()
            return HttpResponseRedirect(request.path_info)
    comments = Comment.objects.filter(post=post)
    context = {
        "post": post,
        "comments": comments,
        "form": CommentForm(),
    }

    return render(request, "blog/detail.html", context)


def add_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('blog_detail', pk=post.pk)
    else:
        form = PostForm()
        #print(form)
    return render(request, 'blog/add_post.html', {'form': form})

