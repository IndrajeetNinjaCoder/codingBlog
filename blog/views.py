from django.shortcuts import render, HttpResponse
from .models import Post


def blogHome(request):
    posts = Post.objects.all()
    return render(request, 'blog/blogHome.html', {'posts':posts})

def blogPost(request, slug):
    post = Post.objects.filter(slug=slug)
    # print(post[0].timeStamp.date)
    return render(request, 'blog/blogPost.html', {'post': post[0]})

