from django.shortcuts import render,HttpResponseRedirect,redirect
from .forms import SignUpForm,LoginForm,PostForm
from  django.contrib  import  messages
from django.contrib.auth import authenticate, login,logout
from .models import  blog_post
from django.contrib import messages
from django.contrib.auth.models import Group



# Create your views here.
#home_page

def home(request):
    posts = blog_post.objects.all()
    return render(request, 'blog/home.html', {"posts": posts})

#abhout page
def about(request):
    return render (request,'blog/about.html')
#contact_page

def contact(request):
    return render(request,'blog/contact.html')
#logout.page
def user_logout(request):
        logout(request)
        return HttpResponseRedirect('/')

    
#dashboard_page
# views.py
# views.py
from django.shortcuts import render, HttpResponseRedirect
from .models import blog_post

def dashboard(request):
    if request.user.is_authenticated:
        posts = blog_post.objects.all()
        user = request.user
        full_name = user.get_full_name()
        gps = user.groups.all()
        return render(request, 'blog/dashboard.html', {'posts': posts, 'full_name': full_name, 'groups': gps})
    else:
        return HttpResponseRedirect('/userlogin/')


#Login_page
def userlogin(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, "Logged in successfully")
                return HttpResponseRedirect('/dashboard/')
            else:
                # Authentication failed
                messages.error(request, 'Invalid username or password.')
        else:
            # Form is not valid, display the form with errors
            messages.error(request, 'Invalid form submission. Please check your inputs.')
    else:
        form = LoginForm()

    return render(request, 'blog/login.html', {'form': form})
#signup_page

from django.urls import reverse

def user_signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Signup successful. Please login.')

            user= form.save()
            group = Group.objects.get(name='Author')
            user.groups.add(group)

            # return redirect('user_login')  # Update 'user_login' to your actual login URL name
        else:
            messages.error(request, 'Signup failed. Please check your inputs.')

    else:
        form = SignUpForm()

    return render(request, 'blog/signup.html', {'form': form})
#add new pos

def add_post(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                desc = form.cleaned_data['desc']
                pst = blog_post(title=title, desc=desc)
                pst.save()
                form = PostForm()  # Reset the form after successful submission
                messages.success(request, 'Post successfully submitted!')

            else:
                # Form is not valid, display errors
                form = PostForm()
        else:
            form = PostForm()

        return render(request, 'blog/addpost.html', {'form': form})
    else:
        return HttpResponseRedirect('/userlogin/')
    #update edit

def update(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = blog_post.objects.get(pk=id)
            form = PostForm(request.POST, instance=pi)
            if form.is_valid():
                form.save()
        else:
            pi = blog_post.objects.get(pk=id)
            form = PostForm(instance=pi)
        return render(request, 'blog/updatepost.html', {'form': form, 'post_id': id})
    else:
        return HttpResponseRedirect('/userlogin/')


#form delete
def delete(request, id):
    if request.user.is_authenticated:
        # Check if the request method is POST
        if request.method == 'POST':
            # Retrieve the blog post or return a 404 response if it doesn't exist
            pi = blog_post.objects.get(pk=id)
            pi.delete()
            # Redirect to the dashboard or any other appropriate page
            return HttpResponseRedirect('/dashboard/')
    else:
        # Redirect to the login page if the user is not authenticated
        return HttpResponseRedirect('/userlogin/')  # local variable 'pi' referenced before assignment

