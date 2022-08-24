from django.shortcuts import render, HttpResponse, redirect
from .models import Post, BlogComment
from django.contrib import messages


def blogHome(request):
    posts = Post.objects.all()
    return render(request, 'blog/blogHome.html', {'posts':posts})

def blogPost(request, slug):
    post = Post.objects.filter(slug=slug).first()
    comments = BlogComment.objects.filter(post=post, parent=None)
    reqlies = BlogComment.objects.filter(post=post).exclude(parent=None)
    params = {'post': post, 'comments':comments, 'replies':reqlies}
    return render(request, 'blog/blogPost.html', params)

def postComment(request):
    if request.method == 'POST':
        comment = request.POST['comment']
        user = request.user
        postSno = request.POST['postSno']
        post = Post.objects.get(sno=postSno)
        parentSno = request.POST['parentSno']

        if parentSno == "":
            comment = BlogComment(comment=comment, user=user, post=post)
            comment.save()
            messages.success(request, "Your comment has been posted successfully")
        else:
            parent = BlogComment.objects.get(sno=parentSno)
            comment = BlogComment(comment=comment, user=user, post=post, parent=parent)
            comment.save()
            messages.success(request, "Your Reply has been posted successfully")

    return redirect(f"/blog/{post.slug}")

