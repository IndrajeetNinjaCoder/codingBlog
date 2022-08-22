from email.policy import default
from django.shortcuts import render, HttpResponse
from blog.models import Post
from home.models import Contact
from django.contrib import messages

# Create your views here.
def home(request):
    return render(request, 'home/home.html')

def about(request):
    return render(request, 'home/about.html')

def contact(request):
    if request.method == 'POST':
        # Oridnary Way to getting form data
        # name = request.POST.get('name', default="")
        # email = request.POST.get('email', default="")
        # phone = request.POST.get('phone', default="")
        # content = request.POST.get('content', default="")

        # New and easy Way to getting form data
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']

        if len(name) < 2 or len(email) < 3 or len(phone) < 10 or len(content) < 4:
            messages.error(request, "Please fill the form currectly")
        
        else:
            contact = Contact(name=name, email=email, phone=phone, content=content)
            contact.save()
            messages.success(request, "your message has been succefully sent")

    return render(request, 'home/contact.html')

def search(request):
    query = request.GET['query']

    if len(query) > 78:
        posts = Post.objects.none()
    else:
        posts = Post.objects.filter(author__icontains=query)
        posts = Post.objects.filter(title__icontains=query)
        posts = Post.objects.filter(content__icontains=query)

    if posts.count() == 0:
        messages.warning(request, "No Search results found. Please refine your query.")

    return render(request, 'home/search.html', {'posts': posts, 'query':query})

