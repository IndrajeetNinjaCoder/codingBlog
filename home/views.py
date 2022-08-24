from email.policy import default
from django.shortcuts import render, HttpResponse, redirect
from blog.models import Post
from home.models import Contact
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# HTML Pages
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

# Authentication APIs 
def handleSignup(request):
    if request.method == 'POST':
        # Get the post parameters 
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        # Checks for errorneous input
        if len(username) > 15:
            messages.error(request, "Username must be under 10 characters")
            return redirect('home')

        if not username.isalnum():
            messages.error(request, "Username should contain letters and numbers")
            return redirect('home')

        if pass1 != pass2:
            messages.error(request, "Passwords do not match")
            return redirect('home')


        # Create the user 
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, "Your account has been successfully created")
        return redirect('home')

    else:
        return HttpResponse('404 Not Found')

def handleLogin(request):
    if request.method == 'POST':
        loginusername = request.POST['loginusername']
        loginpass = request.POST['loginpass']
        user = authenticate(username=loginusername, password=loginpass)

        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect('home')
        else:
            messages.error(request, "Invalid Credentials, Please try again")
            return redirect('home')

    return HttpResponse('404 Not Found')
    
def handleLogout(request):
    logout(request)
    messages.success(request, "Successfully Logged Out")
    return redirect('home')

